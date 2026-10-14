#!/usr/bin/env python3
"""Strict pre-label EX58-X01 fulfillment/reference checks. Standard library only.
Usage: python validate_ex58_x01_fulfillment.py CORRECTED_ROOT REPORT.json
Requires EX58_REFERENCE_AMENDMENT_HASHES.json in this package.
No candidate writes; report must not exist. Run before review-label normalization.
"""
import copy,hashlib,json,sys
from pathlib import Path
B='DescentReviewChanges/ReviewBible'
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    root,report=map(Path,sys.argv[1:]);pack=Path(__file__).resolve().parent
    if report.exists():raise SystemExit('Report exists; refusing overwrite')
    reference=load(pack/'EX58_REFERENCE_AMENDMENT_HASHES.json');manifest=load(root/'EX58_EXACT_FILE_MANIFEST.json')
    checks=[]
    def check(name,ok,kind):checks.append({'id':f'XF-{len(checks)+1:03}','name':name,'passed':bool(ok),'kind':kind})
    check('Original outer manifest unchanged',info(root/'EX58_EXACT_FILE_MANIFEST.json')['sha256']=='d79469ef1ad372fbe156cef094c59ecb9bfae827b389b3041de3f5c6b74a03e5','hash binding')
    for p,binding in manifest['files'].items():
        expected=reference['changedFiles'][p]['referenceDescendant'] if p in reference['changedFiles'] else binding
        check('Exact pre-label file '+p,info(root/p)==expected,'strict complete-byte comparison')
    pub=load(root/B/'data/public/expedition_candidate/complete_candidate.json')
    c=pub['reading']['boundaryCases'][12]
    check('Full corrected EX-W13 object',c==load(pack/'EX_W13_CORRECTED_REFERENCE.json'),'complete record equality')
    m,d=c['records']['ongoingEffect'],c['records']['ownTurn']
    def valid_m(v):return v['classLevel']==3 and 0<=v['RPAfter']<=v['RPBefore']<=8 and v['RPBefore']-v['RPAfter']==3
    def valid_d(v):return v['classLevel']==8 and v['RPPrice']==2 and 0<=v['RPAfter']<=v['RPBefore']<=7 and v['RPBefore']-v['RPAfter']==2
    check('Mage8 to5 legal quoted debit',valid_m(m),'reference fixture')
    check('Dragoon7 to5 legal quoted debit',valid_d(d),'reference fixture')
    trials=[('Original Mage10 to7',valid_m,{**m,'RPBefore':10,'RPAfter':7}),('Original Dragoon10 to8',valid_d,{**d,'RPBefore':10,'RPAfter':8}),('Underfunded Mage2 minus3',valid_m,{**m,'RPBefore':2,'RPAfter':-1}),('Underfunded Dragoon1 minus2',valid_d,{**d,'RPBefore':1,'RPAfter':-1}),('Counterfeit movement RP discount',valid_d,{**d,'RPPrice':1,'RPAfter':6}),('No debit from Mage',valid_m,{**m,'RPAfter':8}),('Unannounced Mage level change',valid_m,{**m,'classLevel':4}),('Unannounced Dragoon level change',valid_d,{**d,'classLevel':9})]
    for name,fn,obj in trials:check('Reject '+name,not fn(obj),'deliberate-corruption reference rejection')
    check('Same movement20 after20ft dismount',d['walkingSpeedFt']==40 and d['dismountCostFt']==20 and d['actualSelfPoweredPathFt']==20 and d['remainingMovementFt']==0,'unchanged consequence')
    check('One Momentum and zero new Dissonance',d['MomentumAfter']==1 and d['DissonanceAfter']==2 and d['baseGain']-d['movementReduction']==0,'unchanged consequence')
    check('Exact original expected outcomes retained',c['expectedOutcomes']=={'carried20Momentum':0,'carried20Discount':0,'own20Momentum':1,'own20DissonanceReduction':1,'RPDiscount':0},'unchanged consequence')
    check('No runtime/selection enabled',pub['selectionEnabled'] is False and pub['runtimeImplemented'] is False,'scope')
    result={'reviewId':'EX58-EXACT-2026-10-11','correction':'EX58-X01','checks':len(checks),'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'details':checks,'classification':'Executed strict-byte, source-bound arithmetic and small deliberate-corruption reference checks. Not a full spell, class, expedition or application runtime. Run on the corrected pre-label tree; later authorized wrapper labels require a separate inverse proof.'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['checks','passed','failed']},indent=2))
    if result['failed']:raise SystemExit(1)
if __name__=='__main__':main()
