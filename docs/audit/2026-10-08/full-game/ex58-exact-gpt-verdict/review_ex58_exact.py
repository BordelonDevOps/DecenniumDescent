#!/usr/bin/env python3
"""Read-only EX58 candidate checks. Standard library only.

Usage: python review_ex58_exact.py ROOT ORIGINAL_ZIP REPORT.json
No gameplay runtime, campaign authentication, or semantic-review replacement.
REPORT must not already exist. Source/candidate input files are never written.
"""
import argparse, base64, collections, hashlib, importlib.util, json, re, zipfile
from fractions import Fraction
from pathlib import Path

B = 'DescentReviewChanges/ReviewBible'
PD = B+'/data/public/expedition_candidate/'
ID = B+'/data/director/expedition_candidate/'
MD = B+'/docs/mechanics/expedition/'
CHANGED = {PD+'boundary_records.json', ID+'boundary_records.json',
           PD+'complete_candidate.json',ID+'complete_candidate.json',
           MD+'EXPEDITION_BOUNDARY_WALKTHROUGHS.md', MD+'EXPEDITION_BOUNDARY_RECORDS.md',
           MD+'EXPEDITION_PLAYER_BOOK.md', MD+'EXPEDITION_DIRECTOR_BOOK.md'}
SUBMISSION_SHA = 'ab16fff6b7e80d755a6b4d1971c9d7e8fbe20442a1876178073b7f546edd946a'
MANIFEST_SHA = 'd79469ef1ad372fbe156cef094c59ecb9bfae827b389b3041de3f5c6b74a03e5'

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def frac(v):
    if isinstance(v,dict): return Fraction(v['numerator'],v['denominator'])
    return Fraction(str(v))
def walk(v,path=''):
    yield path,v
    if isinstance(v,dict):
        for k,x in v.items(): yield from walk(x,path+'/'+str(k).replace('~','~0').replace('/','~1'))
    elif isinstance(v,list):
        for k,x in enumerate(v): yield from walk(x,path+'/'+str(k))
def load_module(path):
    spec=importlib.util.spec_from_file_location('ex58_readonly_renderer',path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def review(root,archive):
    checks=[]
    def check(name,condition,category,evidence=None):
        checks.append(dict(id=f'R{len(checks)+1:04d}',name=name,category=category,
                           passed=bool(condition),evidence=evidence))
    def equal(name,actual,expected,category):
        check(name,actual==expected,category,{'actual':actual,'expected':expected})
    check('Original archive SHA256',sha(archive.read_bytes())==SUBMISSION_SHA,'immutable integrity')
    with zipfile.ZipFile(archive) as z:
        mb=z.read('EX58_EXACT_FILE_MANIFEST.json'); man=json.loads(mb)
        check('Outer manifest SHA256',sha(mb)==MANIFEST_SHA,'immutable integrity')
        equal('419 declared payloads',len(man['files']),419,'immutable integrity')
        equal('420 unique ZIP members',len(set(z.namelist())),420,'immutable integrity')
        for p,rec in man['files'].items():
            data=z.read(p)
            check('Submitted payload '+p,len(data)==rec['bytes'] and sha(data)==rec['sha256'],'immutable integrity')
        amended=[]
        for p,rec in man['files'].items():
            actual=(root/p).read_bytes(); same=len(actual)==rec['bytes'] and sha(actual)==rec['sha256']
            if not same: amended.append(p)
            check('Working input preserved or named descendant '+p,same or p in CHANGED,'working-tree preservation')
        check('No unlisted descendants',set(amended)<=CHANGED,'working-tree preservation',amended)
        v3=read(root/'FILE_MANIFEST.json')
        equal('V3 manifest entries',len(v3),304,'V3 preservation')
        for p,rec in v3.items():
            raw=(root/p).read_bytes()
            check('Frozen V3 '+p,len(raw)==rec['bytes'] and sha(raw)==rec['sha256'],'V3 preservation')
    public=read(root/(PD+'complete_candidate.json')); internal=read(root/(ID+'complete_candidate.json'))
    renderer=load_module(root/B/'tools/assemble_ex58_exact_candidate.py')
    for name,component in public['components'].items():
        equal('Public component '+name,component,internal['completeComponents'][name]['publicEnvelope'],'full projection')
        equal('Standalone public '+name,read(root/(PD+name+'.json')),component,'full projection')
        equal('Standalone internal '+name,read(root/(ID+name+'.json')),internal['completeComponents'][name],'full projection')
    equal('Whole current reading',public['reading'],renderer.current_reading(public['components']),'full projection')
    equal('Whole player rendering',(root/(MD+'EXPEDITION_PLAYER_BOOK.md')).read_text(),renderer.render_player(public),'full rendering')
    equal('Whole Director rendering',(root/(MD+'EXPEDITION_DIRECTOR_BOOK.md')).read_text(),renderer.render_director(internal),'full rendering')
    for p,rec in internal['componentBindings'].items():
        raw=(root/p).read_bytes()
        check('Current component binding '+p,sha(raw)==rec['sha256'] and len(raw)==rec['bytes'],'current reference binding')
    reading=public['reading']; flow=reading['integratedFlow']
    qids=[s['id'] for ch in reading['chapters'] for s in ch['sections']]
    expected=[f'FL-{i:02d}' for i in range(1,27)]+[f'SO-{i:02d}' for i in range(1,13)]+[f'TR-{i:02d}' for i in range(1,15)]+[f'RP-A{i:02d}' for i in range(1,7)]
    equal('All 58 unique directions',sorted(qids),sorted(expected),'coverage')
    for name,key,n in [('chapters','chapters',6),('transport','transportProfiles',29),('auxiliaries','auxiliaryProfiles',4),('boundaries','boundaryCases',28),('social','socialCases',24),('backgrounds','backgroundStartingRules',20)]:
        equal('Count '+name,len(reading[key]),n,'coverage')
    example_count=0
    for i in range(1,7):
        d=internal['completeComponents'][f'part{i:02d}']['directorModule']
        example_count+=len(d['workedCases'])+sum(len(f['cases']) for f in d.get('familyCases',[]))
    equal('190 actual chapter examples',example_count,190,'coverage')
    equal('21 integrated events',len(flow['events']),21,'coverage')
    equal('15 EC contract instances',sorted(flow['contractInstances']),[f'EC-{i:02d}' for i in range(1,16)],'coverage')
    forbidden={'resonanceTrack','fullOriginalFactionRecords','privateSyntheticRivalFrameForW27','completeClassDatasetEnvelopes','originalGPTIntegratedSequence','fearedDisclosure','backer'}
    leaks=[ptr+'/'+k for ptr,obj in walk(public) if isinstance(obj,dict) for k in obj if k in forbidden]
    equal('Private structural keys not projected',leaks,[],'audience boundary')
    equal('No runtime selection',public['selectionEnabled'],False,'scope')
    for k in ['newPromotions','sourceInformationDeleted','runtimeImplemented','humanPlaytestConfirmed','wholeGameFlowConfirmed','pushPerformed','cosmologyReviewed']:
        equal('Scope '+k,internal[k],0 if k in ['newPromotions','sourceInformationDeleted'] else False,'scope')
    # Independent exact arithmetic from instantiated chronology (not an event runtime).
    moving=flow['route']['movingIntervals']
    equal('Outbound moving time',sum(x['endSeconds']-x['startSeconds'] for x in moving[:2]),28800,'flow reference')
    equal('Return moving time',sum(x['endSeconds']-x['startSeconds'] for x in moving[2:]),28800,'flow reference')
    for a,b in [(0,1800),(43200,45000)]:
        check('Stationary feeding interval '+str((a,b)),all(max(a+86400,x['startSeconds'])>=min(b+86400,x['endSeconds']) for x in moving),'flow reference')
    equal('Net feeding change seconds',1800+1800-60,3540,'flow reference')
    equal('Haven entry seconds',flow['events'][11]['relativeEnd'],62592,'flow reference')
    equal('Haven entry clock',f'{62592//3600:02}:{62592%3600//60:02}:{62592%60:02}','17:23:12','flow reference')
    burns=sorted(flow['lighting']['burns'],key=lambda x:x['relativeStart'])
    equal('Light start',burns[0]['relativeStart'],0,'fuel reference')
    equal('Light end',burns[-1]['relativeEnd'],172800,'fuel reference')
    for i,b in enumerate(burns):
        check('Fuel rate '+b['id'],frac(b['pints'])==Fraction(b['relativeEnd']-b['relativeStart'],21600),'fuel reference')
        if i: equal('Continuous light '+b['id'],b['relativeStart'],burns[i-1]['relativeEnd'],'fuel reference')
    check('Exactly eight original oil pints',sum(frac(b['pints']) for b in burns)==8,'fuel reference')
    for r in flow['lighting']['refills']:
        equal('Actual refill duration '+r['id'],r['relativeEnd']-r['relativeStart'],60,'fuel reference')
        check('No simultaneous moving refill '+r['id'],all(max(r['interval']['startSeconds'],m['startSeconds'])>=min(r['interval']['endSeconds'],m['endSeconds']) for m in moving),'fuel reference')
    lots={x['id']:frac(x['amount']) for x in flow['provisions']['lots']}
    totals=collections.defaultdict(Fraction)
    for c in flow['consumption']:
        totals[c['lotId']]+=frac(c['amount'])
        check('Consumption clock '+c['id'],c['interval']['startSeconds']==86400+c['relativeStart'] and c['interval']['endSeconds']==86400+c['relativeEnd'] and c['relativeEnd']>c['relativeStart'],'consumption reference')
    for lot,q in totals.items(): check('Finite consumed total '+lot,q==lots[lot],'consumption reference')
    stock_map={'humanFoodLb':'food-0','humanWaterPints':'water-human-0','muleFeedLb':'feed-0','muleWaterPints':'water-mule-0','sundriesLb':'sundries-0'}
    for n,e in enumerate(flow['events']):
        t=e['relativeEnd']
        check('Event time/version '+e['id'],e['time']['elapsedSeconds']==86400+t and e['version']==n+1 and e['expectedPredecessorVersion']==n,'flow reference')
        for key,lot in stock_map.items():
            used=sum((frac(c['amount']) for c in flow['consumption'] if c['lotId']==lot and c['relativeEnd']<=t),Fraction())
            check('Event stock '+e['id']+'/'+key,frac(e['stateAfter']['oldPhysicalStockRemaining'][key])==lots[lot]-used,'flow reference')
        check('Event oil '+e['id'],frac(e['stateAfter']['oldPhysicalStockRemaining']['oilPints'])==8-Fraction(t,21600),'fuel reference')
    cash=flow['money']['startingCapitalCp']
    for tx in flow['money']['transactions']:
        q=frac(tx['exactCp']); purchase=tx['payer']=='Expedition cash'
        expected_cp=-(-q.numerator//q.denominator) if purchase else q.numerator//q.denominator
        equal('Transaction rounding '+tx['transactionId'],tx['settledCp'],expected_cp,'money reference')
        cash+=tx['settledCp']*(-1 if purchase else 1)
        check('No fictional credit '+tx['transactionId'],cash>=0,'money reference')
    equal('Final actual cash',cash,4480,'money reference')
    settle=flow['money']['settlement']
    formula_values={'sponsorBaseCp':12000-600-200,'sponsorCp':(12000-600-200)//5,'netCp':12000-600-200-2240,'trueProfitCp':8960-2020,'distributionCp':6940-2000,'eachCharacterCp':4940//4,'cashAfterDistributionCp':9940-4940,'finalCashCp':5000-520,'unspentEarmarkCp':2000-520}
    for k,v in formula_values.items(): equal('Settlement '+k,settle[k],v,'money reference')
    rest=flow['rest']
    for k in ['actualFirst','secondActual']: equal('Rest duration '+k,rest[k]['endSeconds']-rest[k]['startSeconds'],28800,'rest reference')
    equal('First Rest completion relative',rest['actualFirst']['endSeconds']-86400,104592,'rest reference')
    equal('First Rest clock',f'{104592//3600:02}:{104592%3600//60:02}:{104592%60:02}','29:03:12','rest reference')
    equal('Sleep excludes light activity',rest['firstRestSleepSeconds'],28800-sum(x['endSeconds']-x['startSeconds'] for x in rest['firstRestLightActivity']),'rest reference')
    check('Sleep at least six hours',rest['firstRestSleepSeconds']>=21600,'rest reference')
    check('First beneficial completion at least 24 hours',rest['actualFirst']['endSeconds']-rest['previousBeneficialCompletion']['elapsedSeconds']>=86400,'rest reference')
    equal('Second Rest does not reset resources',rest['secondBeneficial'],False,'rest reference')
    equal('Completion separation',rest['secondActual']['endSeconds']-rest['actualFirst']['endSeconds'],68208,'rest reference')
    check('Debt cleared before deadline',rest['debtEvents'][1]['time']['elapsedSeconds']<rest['debtEvents'][0]['deadline']['elapsedSeconds'],'rest reference')
    reservations=collections.defaultdict(list)
    for r in flow['actorReservations']: reservations[r['actor']].append(r)
    for actor,rows in reservations.items():
        clashes=[]
        for i,a in enumerate(rows):
            for b in rows[i+1:]:
                if max(a['start'],b['start'])<min(a['end'],b['end']): clashes.append([a,b])
        equal('No incompatible declared reservation overlap '+actor,clashes,[],'actor reference')
    wp=flow['nextProcurement']['waterFilling']
    equal('Four workers, 28 distinct skins',len({s for l in wp['assignment'].values() for s in l}),28,'procurement reference')
    equal('Elapsed parallel filling',wp['elapsedMinutes'],max(len(l) for l in wp['assignment'].values())*wp['minutesPerSkin'],'procurement reference')
    equal('Paid stock distinct from old depletion',flow['nextProcurement']['oldOilAtDeparturePints'],0,'procurement reference')
    p6=internal['completeComponents']['part06']
    for f in p6['syntheticRawFixtures']:
        raw=base64.b64decode(f['rawBase64'],validate=True)
        check('Raw fixture bytes/hash '+f['id'],len(raw)==f['bytes'] and sha(raw)==f['sha256'],'raw history reference')
    for i,s in enumerate(p6['syntheticReferenceSceneRecords']):
        proposal=sum(s['proposals']); applied=max(-2,min(2,proposal)); beforeclip=s['opening']+applied; result=max(-3,min(3,beforeclip))
        equal('Signed scene '+str(i),[s['sceneProposal'],s['sceneAppliedProposal'],s['sceneOverflow'],s['scaleOverflow'],s['result'],s['deltaFromOpening']],[proposal,applied,proposal-applied,beforeclip-result,result,result-s['opening']],'standing reference')
    for book in ['EXPEDITION_PLAYER_BOOK.md','EXPEDITION_DIRECTOR_BOOK.md']:
        path=root/(MD+book); text=path.read_text()
        for i,target in enumerate(re.findall(r'\[[^\]]*\]\(([^)]+)\)',text)):
            if '://' in target: continue
            name,sep,anchor=target.partition('#'); tp=(path.parent/name).resolve() if name else path
            exists=tp.exists()
            if exists and anchor and tp.suffix=='.md':
                tt=tp.read_text(); explicit=re.findall(r'<a id="([^"]+)"',tt)
                headings=[re.sub(r'[^\w\- ]','',s.lower()).replace(' ','-') for s in re.findall(r'^#+\s+(.*)$',tt,re.M)]
                exists=anchor in explicit+headings
            check('Reading link '+book+'/'+str(i),exists,'navigation',target)
    # The one confirmed semantic defect: actual selected class tables, not invented pool capacity.
    mage=(root/B/'docs/mechanics/classes/mage.md').read_text()
    dragoon=(root/B/'docs/mechanics/classes/dragoon.md').read_text()
    def table_rp(text,level):
        rows=[s.strip() for s in text.splitlines() if s.strip().startswith('|')]
        header=next(s for s in rows if 'RP maximum' in s)
        cells=[s.strip() for s in header.strip('|').split('|')]
        col=next(i for i,s in enumerate(cells) if 'RP' in s)
        row=next(s for s in rows if re.match(r'^\|\s*'+str(level)+r'\s*\|',s))
        return int(row.strip('|').split('|')[col].strip())
    # Tables have an exact explicit level / maximumRP column; fail rather than invent a fallback.
    max_m,max_d=table_rp(mage,3),table_rp(dragoon,8)
    equal('Mage3 controlling maximum',max_m,8,'source class reference')
    equal('Dragoon8 controlling maximum',max_d,7,'source class reference')
    c=reading['boundaryCases'][12]; equal('Exact boundary ID',c['id'],'EX-W13','source class reference')
    m=c['records']['ongoingEffect']; d=c['records']['ownTurn']
    check('EX58-X01 Mage pool admits and pays actual 3 RP',0<=m['RPAfter']<=m['RPBefore']<=max_m and m['RPBefore']-m['RPAfter']==3,'confirmed semantic-reference defect',{'maximum':max_m,'before':m['RPBefore'],'after':m['RPAfter']})
    check('EX58-X01 Dragoon pool admits and pays actual 2 RP',0<=d['RPAfter']<=d['RPBefore']<=max_d and d['RPBefore']-d['RPAfter']==2,'confirmed semantic-reference defect',{'maximum':max_d,'before':d['RPBefore'],'after':d['RPAfter']})
    equal('Dismount and actual walking exhaust 40ft',d['dismountCostFt']+d['actualSelfPoweredPathFt']+d['remainingMovementFt'],40,'boundary reference')
    equal('Movement discounts Dissonance not RP',[d['RPPrice'],d['baseGain']-d['movementReduction'],d['DissonanceAfter']],[2,0,2],'boundary reference')
    # Report only compact evidence for large successful object-equality checks.
    for c in checks:
        if c['passed'] and c['category'] in {'full projection','full rendering'}: c['evidence']={'fullObjectEquality':True}
    return {'reviewId':'EX58-EXACT-2026-10-11','submissionSha256':SUBMISSION_SHA,'manifestSha256':MANIFEST_SHA,
            'workingRoot':str(root),'checks':len(checks),'passed':sum(c['passed'] for c in checks),
            'failed':sum(not c['passed'] for c in checks),'categories':dict(collections.Counter(c['category'] for c in checks)),
            'failureDetails':[c for c in checks if not c['passed']],'namedDescendantPaths':amended,
            'checksAre':'Read-only byte/whole-object/render/source-reference and rational arithmetic checks; not a gameplay runtime or campaign authentication.',
            'details':checks}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('archive',type=Path); ap.add_argument('report',type=Path); args=ap.parse_args()
    if args.report.exists(): raise SystemExit('Refusing to overwrite existing report')
    result=review(args.root.resolve(),args.archive.resolve())
    args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['checks','passed','failed','categories']},indent=2))
    for f in result['failureDetails']: print(f['name'],str(f['evidence'])[:800])
if __name__=='__main__': main()
