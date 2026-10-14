"""Read-only finite checks of LAX-01--03 proposed corrections.
Usage: python verify_lax_named_corrections.py SUBMISSION CORRECTED --output REPORT
No game runtime is called. Value checks are reference-contract fixtures; device checks
compare actual supplied source profiles and authored scope, not executed gameplay.
"""
from pathlib import Path
import argparse,hashlib,json,re
B='DescentReviewChanges/ReviewBible';A='docs/audit/2026-10-08/full-game'
P=B+'/data/playtest/language_communication_candidate_public.json';I=B+'/data/director/language_communication_candidate_internal.json'
G=B+'/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md';IG=B+'/docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md';WG=B+'/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md';C=A+'/LANGUAGE_CANDIDATE_WORKED_ADJUDICATIONS.json'
MISSING=object()
def original_value_valid(record,original=MISSING):
    """Reference meaning of LAX-02, not an authenticated source/production schema."""
    state=record.get('fieldPresence');has='sourceSpelling' in record
    if original is MISSING:return state=='absent' and not has
    if original is None:return state=='null' and has and record['sourceSpelling'] is None
    if state!='value' or not has or record['sourceSpelling'] is None:return False
    # Avoid treating JSON true and 1 as identical. This does not authenticate the source.
    return json.dumps(record['sourceSpelling'],sort_keys=True,ensure_ascii=False,allow_nan=False)==json.dumps(original,sort_keys=True,ensure_ascii=False,allow_nan=False)
def run(frozen,current,spec_path):
    def read(root,p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
    def text(root,p):return (root/p).read_text(encoding='utf-8-sig')
    def same(p):return (frozen/p).read_bytes()==(current/p).read_bytes()
    pub=read(current,P);priv=read(current,I);oldpub=read(frozen,P);oldpriv=read(frozen,I)
    spec=json.loads(spec_path.read_text());changes=spec['corrections'];checks=[]
    def add(name,ok,kind='static/source comparison',detail=None):
        r={'id':f'LAX-F{len(checks)+1:02d}','name':name,'kind':kind,'passed':bool(ok),'runtimeTest':False}
        if detail is not None:r['detail']=detail
        checks.append(r)
    guide=text(current,G)
    add('Both LAX-01 replacement paragraphs exact',all(x['replacement'] in guide and x['old'] not in guide for x in changes[0]['affected'] if 'replacement' in x))
    links=[]
    for p in [G,WG,IG]:
        for link in re.findall(r'\]\(([^)]+)\)',text(current,p)):
            if '://' in link:continue
            f,_,a=link.partition('#');dest=(current/p).parent/f if f else current/p
            links.append((str(dest),dest.exists()))
    add('All 12 active manuscript link occurrences resolve',len(links)==12 and all(ok for _,ok in links),detail=links)
    add('Full public guideText equals corrected manuscript',pub['guideText']==guide)
    cases=read(current,C)['cases'];seq=text(current,WG)
    seq_ok=True
    for c in cases:
        block=seq.split('## '+c['id']+' — ',1)[1].split('\n## ',1)[0]
        seq_ok &= c['setup'] in block and c['adjudicatedOutcome'] in block and all(x['event'] in block for x in c['chronology'])
    add('All 32 full chronological sequences match both envelopes and manuscript',seq_ok and pub['workedAdjudications']==priv['workedAdjudications']==cases)
    expected_prov=changes[1]['affected'][0]['replacement']
    add('Exact conditional provenance contract in both envelopes',pub['recordSchema']['definitions']['provenance']==priv['recordSchema']['definitions']['provenance']==expected_prov)
    fixtures=[
      ('absent/omitted accepted',{'fieldPresence':'absent'},MISSING,True),
      ('absent/null rejected',{'fieldPresence':'absent','sourceSpelling':None},MISSING,False),
      ('absent/empty rejected',{'fieldPresence':'absent','sourceSpelling':''},MISSING,False),
      ('null/null accepted',{'fieldPresence':'null','sourceSpelling':None},None,True),
      ('null/omitted rejected',{'fieldPresence':'null'},None,False),
      ('null/empty rejected',{'fieldPresence':'null','sourceSpelling':''},None,False),
      ('value/exact spelling accepted',{'fieldPresence':'value','sourceSpelling':'Orc'},'Orc',True),
      ('value/empty string retained',{'fieldPresence':'value','sourceSpelling':''},'',True),
      ('value/empty array retained',{'fieldPresence':'value','sourceSpelling':[]},[],True),
      ('value/empty object retained',{'fieldPresence':'value','sourceSpelling':{}},{},True),
      ('value/omitted rejected',{'fieldPresence':'value'},'Orc',False),
      ('value/null rejected',{'fieldPresence':'value','sourceSpelling':None},'Orc',False),
      ('canonical spelling cannot replace source spelling',{'fieldPresence':'value','sourceSpelling':'Orcish'},'Orc',False),
      ('JSON boolean is not numeric source value',{'fieldPresence':'value','sourceSpelling':True},1,False),
    ]
    for name,r,o,want in fixtures:add(name,original_value_valid(r,o)==want,'executed reference-contract fixture')
    absent=[x for x in pub['grants']['backgrounds'] if not x['sourceLanguagesFieldPresent']]
    add('All five absent background language values remain absent',len(absent)==5 and all('originalLanguagesSource' not in x for x in absent))
    add('Other seven complete record definitions untouched',all(pub['recordSchema']['definitions'][k]==oldpub['recordSchema']['definitions'][k] for k in pub['recordSchema']['definitions'] if k!='provenance'))
    expected_control=next(x['replacement'] for x in changes[2]['affected'] if x.get('pointer')=='/rules/deviceControl')
    add('Exact TI-04 scope and two action contexts in both envelopes',pub['rules']['deviceControl']==priv['rules']['deviceControl']==expected_control)
    master=read(frozen,B+'/data/director/advanced_craft_recipe_candidate_internal.json');cards={x['recipeId']:x for x in master['cards']}
    groups=changes[2]['internalAffectedRecipeGroups'];kindmap={'ordinaryTI04Automata':'TI-automaton','specialTI04Invocation':'TI-drone','trapsDoNotInheritTI04':'TI-trap','utilitiesDoNotInheritTI04':'TI-utility','directOperatorProfileDoNotInheritTI04':'TI-siege'}
    ti={x['recipeId'] for x in master['cards'] if x['sourceRecipe']['skill']=='Tinkering'}
    ids=[id for x in groups.values() for id in x]
    add('All 43 actual device records have the stated 18/1/11/12/1 scope partition',set(ids)==ti and len(ids)==43 and all(cards[id]['operational']['profile']==kindmap[k] for k,vals in groups.items() for id in vals))
    add('Three ordinary active automata; no silent class-slot merge',expected_control['activeOrdinaryAutomataLimit']==3 and 'class devices keep only their own actual limits' in guide)
    add('684 fixture uses its actual automaton source',cards['recipe-684']['operational']['profile']=='TI-automaton' and 'recipe-684' in cases[29]['setup'] and 'Action start' in cards['recipe-684']['manuscriptText'])
    add('591 retains direct necessary work and one utility charge',cards['recipe-591']['operational']['profile']=='TI-utility' and 'one active minute' in cards['recipe-591']['manuscriptText'] and 'spends one charge' in cards['recipe-591']['manuscriptText'] and 'manually operated utilities' in guide)
    add('585 retains one-minute placement then Action arming, not automaton command',cards['recipe-585']['operational']['profile']=='TI-trap' and 'Spend one minute' in cards['recipe-585']['manuscriptText'] and 'then an Action to arm' in cards['recipe-585']['manuscriptText'])
    add('687 retains three distinct direct-operator Actions',cards['recipe-687']['operational']['profile']=='TI-siege' and 'three distinct successive-or-later own regular turns' in cards['recipe-687']['manuscriptText'] and "not a companion's commanded attack" in cards['recipe-687']['manuscriptText'])
    rendered=json.dumps(pub,ensure_ascii=False)
    add('Private coordinator and ram membership not newly exported','recipe-686' not in rendered and 'recipe-687' not in rendered)
    add('Noncombat programmed-task start remains an Action',expected_control['programmingActiveMinutes']==10 and 'Outside initiative: one Action starts' in expected_control['commandAction'] and 'not the combat Bonus Action command' in guide)
    add('Unchanged task can be registered within initial ten-minute binding',expected_control['initialCompatibleTaskIncludedInBinding'] is True and 'Do not charge a second programming period' in guide)
    add('Existing shared budget, service and failure-refund values retained',all(expected_control[k]==oldpub['rules']['deviceControl'][k] for k in ['sharedBudget','serviceAndRepairHistoryPreserved','committedAllowanceRefundOnFailure']))
    native_sections=oldpriv['completedAdvancedInterfaces']['completeApplicableProcedureSections']
    add('TD-08 eligibility/disable and actual service sections remain exact',all(priv['completedAdvancedInterfaces']['completeApplicableProcedureSections'][k]==native_sections[k] for k in ['TI-04','TI-05','TI-08','TD-01','TD-08']) and 'not limited by this automaton-command scope' in guide)
    add('Corrected T30 exact and no runtime pass flag',cases[29]==next(x['replacement'] for x in changes[2]['affected'] if x.get('pointer')=='/cases[id=LA-T30]') and cases[29]['runtimePassed'] is False)
    add('All other 31 authored sequence objects untouched',[x for x in cases if x['id']!='LA-T30']==[x for x in oldpub['workedAdjudications'] if x['id']!='LA-T30'])
    add('All 16 original directions retained beside named clarifications',all(all(new[k]==v for k,v in old.items()) for old,new in zip(oldpriv['decisionApplicationRegister'],priv['decisionApplicationRegister'])))
    add('49 original class interfaces/statuses untouched',priv['classInterfaces']==oldpriv['classInterfaces'] and pub['classInterfaces']==oldpub['classInterfaces'])
    add('23 spell comparisons, 15 pending routes and 8 pending feats untouched',priv['spellInterfaces']==oldpriv['spellInterfaces'] and priv['pendingInterfaces']==oldpriv['pendingInterfaces'] and pub['spellInterfaces']==oldpub['spellInterfaces'] and pub['pendingFeatInterfaces']==oldpub['pendingFeatInterfaces'])
    add('40 internal and 28 public Scribing records and 19 sections untouched',priv['completedAdvancedInterfaces']==oldpriv['completedAdvancedInterfaces'] and pub['publicScribingCards']==oldpub['publicScribingCards'])
    manifests=read(frozen,'ORIGINAL_SOURCE_V2_FILE_MANIFEST.json')
    add('All 152 original payload bytes unchanged in proposed copy',all(same(p) for p in manifests))
    frozen_m=read(frozen,'FILE_MANIFEST.json')
    add('All 184 submitted payloads still match the frozen manifest',all(hashlib.sha256((frozen/p).read_bytes()).hexdigest()==e['sha256'] for p,e in frozen_m.items()))
    original_code=text(frozen,B+'/tools/validate_language_candidate.py');vpatch=changes[1]['affected'][-1]
    add('Existing validator changes only the named provenance assertion',text(current,B+'/tools/validate_language_candidate.py')==original_code.replace(vpatch['old'],vpatch['replacement']))
    add('No approval flags or LA16 receipt changed',all(pub[k] is False and priv[k] is False for k in ['exactLanguageApproval','classSpellFeatPromotion','runtimeImplemented','humanBalanceApproved','wholeGameFlowApproved']) and priv['deferredReceipt']==oldpriv['deferredReceipt'])
    private_cards=[x for x in oldpriv['completedAdvancedInterfaces']['completeScribingCards'] if x['visibility']!='public']
    add('Private Scribing membership remains absent',all(not re.search(re.escape(c['recipeId'])+r'\b',rendered) and c['name'] not in rendered for c in private_cards))
    return {'reviewId':'LAX-EXACT-2026-10-11','scope':'Reviewer-local proposed correction proof. Static/full-source comparisons and 14 executable reference-contract fixtures only. Not gameplay tests, real campaign facts, owner fulfillment or promotion.','count':len(checks),'passed':sum(c['passed'] for c in checks),'checks':checks,'failed':[c for c in checks if not c['passed']]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('frozen',type=Path);p.add_argument('corrected',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    o=a.output.resolve()
    if any(root.resolve() in o.parents for root in [a.frozen,a.corrected]):raise SystemExit('Report output must be outside both inspected trees.')
    result=run(a.frozen,a.corrected,Path(__file__).with_name('LAX_CORRECTIONS.json'));o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ['count','passed','failed']},indent=2))
if __name__=='__main__':main()
