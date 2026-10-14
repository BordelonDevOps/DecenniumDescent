"""Finite AEX correction gate: full-cohort text/source checks and worked arithmetic.

The 33 cases document authored adjudications. This does not execute or certify
an advanced-item runtime, authenticate campaign facts, or establish balance.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib
import json
import re

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
V = A/'advanced167-exact-reviewer-files'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(G).as_posix()
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    ip=R/'data/director/advanced_craft_recipe_candidate_internal.json'
    pp=R/'data/crafting/advanced_craft_recipe_candidate_public.json'
    d,p=read(ip),read(pp)
    cards={c['recipeId']:c for c in d['cards']}
    public={c['recipeId']:c for c in p['cards']}
    reg=read(V/'AEX_167_CORRECTIONS.json')
    assert sha(V/reg['verdictFile'])==reg['verdictSha256']=='87db8f8b373d497444bbd3b6b43e4dfd0b4eedf4f4239312af7bf513ace3f250'
    specs=read(V/'AEX_167_FOCUSED_REGRESSIONS.json')
    quotes={c['id']:re.findall(r'^> (.+)$',c['completeCorrectionSpecificationMarkdown'],re.M) for c in reg['corrections']}
    ids={c['id']:c['affectedRecipeIds'] for c in reg['corrections']}
    gp=p['operatingGuideText']; bp=p['bodyGuideText']
    source=lambda sid:d['procedureSections'][sid]['text']
    effect=lambda c:next(x['text'] for x in c['operational']['paragraphs'] if x['label']=='Effect and operation')
    para=lambda c,label:next(x['text'] for x in c['operational']['paragraphs'] if x['label']==label)
    allchecks=[]
    def check(name,value,detail=None):
        allchecks.append({'id':name,'pass':bool(value),'detail':detail})
        return bool(value)
    for cid,expected in ids.items():
        actual=[k for k,c in cards.items() if cid in c['operational']['exactReviewCorrections']]
        check(cid+'-membership',set(actual)==set(expected),len(actual))
    check('recipe-counts',len(cards)==167 and len(public)==100)
    check('embedded-guides-equal',gp==(R/p['guide']).read_text(encoding='utf-8') and bp==(R/p['bodyGuide']).read_text(encoding='utf-8'))
    for k,c in cards.items():
        check(k+'-recovery',quotes['AEX-01'][0] in para(c,'Retention and failure') and 'floor(min(Q_i / 4, R_i) / u_i)' in para(c,'Retention and failure'))
        check(k+'-manuscript',all(x['text'] in c['manuscriptText'] for x in c['operational']['paragraphs']))
        if k in public:
            pc=public[k]
            # The accepted public envelope replaces ingredient metadata and omits
            # private history; all operative rule paragraphs must remain exact.
            internal_rules=[x for x in c['operational']['paragraphs'] if x['label'] not in ['Exact component occurrences','Internal source history']]
            public_wording={
                'The full 48-card Tinker interface register and TD-01–18 apply':'The Tinker class-interface procedures in the player guide apply',
                'max three active ordinary crafted automata separately from one 686':'at most three active ordinary crafted automata; class companion/deployable slots keep their separate source limits',
            }
            internal_rules=[dict(x) for x in internal_rules]
            for x in internal_rules:
                for before,after in public_wording.items():x['text']=x['text'].replace(before,after)
            public_rules=[x for x in pc['operational']['paragraphs'] if x['label']!='Required component occurrences']
            check(k+'-public-paragraphs',public_rules==internal_rules and all(x['text'] in pc['manuscriptText'] for x in pc['operational']['paragraphs']))
        if k in ids['AEX-02']:
            if c['operational']['profile']=='TI-trap': ok=quotes['AEX-02'][3] in effect(c)
            else: ok=all(q in para(c,'Rune control and examination') for q in quotes['AEX-02'][:2])
            check(k+'-control',ok)
        if c['operational']['profile']=='RC-binding':check(k+'-binding',quotes['AEX-02'][2] in effect(c))
        if k in ids['AEX-03']:
            check(k+'-service',c['operational']['useBinding']['serviceUnit']==quotes['AEX-03'][0] and quotes['AEX-03'][0] in effect(c))
        if k in ids['AEX-04']:check(k+'-disable',quotes['AEX-04'][0] in para(c,'Routed Dissonance'))
        if k in ids['AEX-05']:check(k+'-jaw',quotes['AEX-05'][0] in para(c,'Complete output bodies'))
        if k in ids['AEX-06']:check(k+'-ward-trigger',c['operational']['useBinding']['trigger']==quotes['AEX-06'][0])
    check('public-common-corrections',all(q in gp for cid in ['AEX-01','AEX-02','AEX-03','AEX-04','AEX-07'] for q in quotes[cid]))
    check('device-model',d['bodyModels']['TI-device']['operationalModelDescription']==quotes['AEX-05'][0] and quotes['AEX-05'][0] in bp)
    # Source/profile fields and all numerical bindings must survive verbatim.
    old=read(A/'advanced167-before-aex-corrections'/rel(ip))
    oldcards={c['recipeId']:c for c in old['cards']}
    for k,c in cards.items():
        prev=oldcards[k]
        check(k+'-preserved-authority',all(c[f]==prev[f] for f in ['sourceRecipe','sourceObjectSha256','sourceAuthoringRegister','publicBookBinding']))
        check(k+'-preserved-numeric-bindings',all(c['operational'][f]==prev['operational'][f] for f in ['standardQuantity','maximumOrderedBodyReserve','work','creation','componentOccurrences','sourceStandardBatchReferenceGp','sourceProcessUnitReferenceGp','bodyVariants','creatureOutput']))
    check('original-procedures-preserved',all(s['text']==old['procedureSections'][k]['text'] for k,s in d['procedureSections'].items()))
    check('original-models-preserved',all(b['sourceAuthoringProfile']==old['bodyModels'][k]['sourceAuthoringProfile'] for k,b in d['bodyModels'].items()))
    refs={'SC-script':['SC-05','SC-01–05','SC-10'],'SC-reference':['SC-04, SC-05, SC-07, SC-08 and SC-10'],'RC-warding':['RC-08 six-second'],'RC-binding':['RC-01–04'],'RC-explosive':['RC-01–03 and RC-05'],'RC-healing':['RC-01–03 and RC-06']}
    reference_ok=True
    for k in ids['AEX-07']:
        c=cards[k]; ok=all(x in effect(c) for x in refs[c['operational']['profile']])
        if c['operational']['profile'].startswith('SC-'):ok=ok and quotes['AEX-07'][0] in effect(c)
        reference_ok=check(k+'-correct-locators',ok) and reference_ok
    # Expand actual public locators and resolve each through its public legend.
    def codes(text):
        result=set()
        for m in re.finditer(r'\b(AC|EN|RC|SC|TI|TD|B)-(\d{2})(?:[–-](\d{2}))?((?:/\d{2})*)',text):
            prefix,start,end,extra=m.groups(); start=int(start)
            nums=range(start,int(end)+1) if end else [start]
            result.update(f'{prefix}-{n:02}' for n in nums)
            result.update(f'{prefix}-{int(n):02}' for n in extra.split('/') if n)
        return result
    legend=gp.split('## Public procedure locator',1)[1]
    public_codes=codes('\n'.join(c['manuscriptText'] for c in public.values()))
    legend_codes=codes(legend)
    headings={re.sub(r'[^a-z0-9 -]','',h.lower()).replace(' ','-') for h in re.findall(r'^## (.+)$',gp,re.M)}
    links=re.findall(r'\]\(([^)]+)\)',legend)
    locator_ok=public_codes<=legend_codes and all(x[1:] in headings if x.startswith('#') else (R/p['bodyGuide']).name==x for x in links)
    check('public-locators-resolve',locator_ok,{'used':sorted(public_codes),'unresolved':sorted(public_codes-legend_codes)})
    check('no-private-procedural-locators',not public_codes.intersection({'RC-10','SC-09','TI-08','TI-09'}))
    existing=[]
    for name,script,countkey,count in [('INTERNAL_CANDIDATE','internal_candidates','checks',5808),('PUBLIC_CANDIDATE','public_candidates','checks',1725),('WORKED_CASE','worked_cases','checkCount',52)]:
        f=A/f'ADVANCED_CRAFT_{name}_VALIDATION.json'; report=read(f)
        valid=report['status'].startswith('PASS') and report[countkey]==count
        if name=='INTERNAL_CANDIDATE':valid=valid and report['candidateSha256']==sha(ip)
        else:valid=valid and report['internalCandidateSha256']==sha(ip)
        if name=='PUBLIC_CANDIDATE':valid=valid and report['publicCandidateSha256']==sha(pp)
        check(name+'-current-report',valid)
        sp=R/f'tools/validate_advanced_craft_{script}.py'
        existing.append({'file':rel(f),'sha256':sha(f),'script':rel(sp),'scriptSha256':sha(sp),'checks':count})
    # These are numerical reference calculations, never live inventory operations.
    def recover(q,remaining,u):return (min(F(q)/4,F(remaining))//F(u))*F(u)
    occurrence=cards['recipe-480']['operational']['componentOccurrences'][2]
    material=occurrence['sourceComponent']; precision=occurrence['defaultFailurePrecision']
    check('480-source-premise',material['quantity']==5 and F(str(material['weight']))==F(1,10) and precision=={'numerator':1,'denominator':100} and occurrence['failedRecoveryEligible'])
    numeric={
        'AEX-01-R01':(recover(5,2,'0.01'),F('1.25'),F('0.125')),
        'AEX-01-R02':(recover(5,'0.60','0.01'),F('0.60'),F('0.06')),
        'AEX-01-R03':(recover(3,3,1),F(0),F(0)),
        'AEX-01-R04':(recover(5,0,'0.01'),F(0),F(0)),
    }
    # Independent explicit clause requirements for the authored sequence cases.
    ground='\n'.join(para(cards[k],'Rune control and examination') for k in ids['AEX-02'] if cards[k]['sourceRecipe']['skill']=='Rune Carving')
    binding=effect(cards['recipe-396']); healing=effect(cards['recipe-422'])+'\n'+source('RC-06')
    service=effect(cards['recipe-684'])+'\n'+source('TI-05')
    routed=para(cards['recipe-595'],'Routed Dissonance')+'\n'+source('TD-08')
    ward=next(c['operational']['useBinding']['trigger'] for c in cards.values() if c['operational']['profile']=='RC-warding')
    requirements={
      'AEX-01-R05':(gp,['Group only genuinely identical eligible inputs within this same batch','retaining every physical occurrence','Catalysts and unrelated batches do not enter']),
      'AEX-02-R01':(ground,['wholly covered','one-Action manual arming','next-regular-start or six-second delay','uncovering, repairing or unsuppressing does not rearm']),
      'AEX-02-R02':(ground,['suppressed cannot trigger','unsuppressing does not rearm']),
      'AEX-02-R03':(ground+'\n'+gp,['Broken','repairing or unsuppressing does not rearm','refill']),
      'AEX-02-R04':(binding,['covering','ends this particular Binding restraint','does not resume that ended restraint']),
      'AEX-02-R05':(binding,['Breaking','Restoring the plate does not resume','refund its charge or rearm']),
      'AEX-02-R06':(source('RC-08')+'\n'+gp,['original expiry still runs','only the remaining original benefit','only the still-unexpired original benefit','no new activation, refunded charge or extended duration']),
      'AEX-02-R07':(ground,['INT (Arcana)','INT check using Runecarver','actual applicable proficiency','unrelated tool proficiency is not a substitute']),
      'AEX-02-R08':(ground+'\n'+gp,['setter can disarm their accessible plate with an Action','unknown accessible Rune requires actual Runecarver','one active minute','original recipe creation DC','setter can safely disarm their accessible trap with one Action',"trained thieves' tools or Tinker's tools",'printed trap save DC']),
      'AEX-02-R09':(healing,['Stationary setup/arming and helper healing are separate Actions','assigned willing or Incapacitated ally within 5 feet','one discharge per physical item per round','specific direct-touch exception','no standing-area trigger']),
      'AEX-03-R01':(service,['Mere encounter start does not debit a stored or otherwise unoperated automaton','spends nothing and grants no active behavior']),
      'AEX-03-R02':(service,['First actual operation','spends one service unit','ten elapsed minutes from that operation']),
      'AEX-03-R03':(service,['Suppression/shutdown keeps the clock running','pause/shutdown/suppression does not refund or extend']),
      'AEX-03-R04':(service,['Zero units inside an already paid block permits that block only','At zero with no remaining paid block','inert']),
      'AEX-03-R05':(service,['entering combat closes the noncombat block and spends a new unit','Continuing past expiry needs another','No benefit from attacking allies','Short/long rest','686 has its distinct winding profile']),
      'AEX-04-R01':(routed,['armed charged trap','prevents movement, attacks, auras, triggers and every other active device use','trap cannot discharge','grant a queued activation','does not refill charges']),
      'AEX-04-R02':(routed,['live eligible task','utility cannot provide its charged task benefit','does not refund a previously legal committed cost']),
      'AEX-04-R03':(routed,['Actual Field Repair','ten-active-minute/1RP','paid service/winding clocks continue','does not refill charges, service, RP or Refrain']),
      'AEX-04-R04':(routed,['up to two current Dissonance into one own active qualifying device within 30 feet',"origin Tinker's next completed genuine short rest","buyer's unrelated rest does not clear",'Transfer retains disable origin, expiry, resource record']),
      'AEX-06-R01':(ward+'\n'+source('RC-07'),["bearer's saving throw, including an area effect",'declare and spend one Reaction and one charge before']),
      'AEX-06-R02':(ward,['An attack legally targets the attuned bearer','before the initiating attack or saving throw is rolled']),
      'AEX-06-R03':(ward,['must declare','before the initiating attack or saving throw is rolled']),
      'AEX-06-R04':(ward,['An attack legally targets','or an actual event requires',"bearer's saving throw"]),
      'AEX-07-R03':(source('SC-05')+'\n'+gp,['lead personally consults','one active minute','no self-production bonus','manufacture or repair','Genuine relevant formula research remains separately eligible without guaranteeing discovery']),
    }
    focused=[]
    for case in specs['cases']:
        cid=case['id']; evidence={}; method='authored adjudication with source-clause and complete-cohort static checks'
        if cid in numeric:
            value,want,mass=numeric[cid];ok=value==want and value*F('0.1')==mass
            evidence={'recoveredSourceUnits':str(value),'recoveredMassLb':str(value*F('0.1')),'divisibleFormIsCasePremise':True};method='exact rational reference arithmetic'
        elif cid.startswith('AEX-05'):
            # Synthetic workpieces test conjunction; other physical predicates are explicit.
            size,weight,expected={'AEX-05-R01':((5,4,2),F('0.5'),False),'AEX-05-R02':((4,4,2),F(3),False),'AEX-05-R03':((4,4,2),F(2),True)}[cid]
            admitted=all(a<=b for a,b in zip(size,(4,4,2))) and weight<=2
            model=d['bodyModels']['TI-device']['sourceAuthoringProfile']
            ok=admitted==expected and model==old['bodyModels']['TI-device']['sourceAuthoringProfile'] and 'both fit' in quotes['AEX-05'][0] and 'Both hands operate it' in d['bodyModels']['TI-device']['operationalBodyText']
            evidence={'syntheticWorkpieceInches':size,'massLb':str(weight),'bothLimitsSatisfied':admitted,'otherHandlingConditionsAssumed':True,'originalBodyProfileUnchanged':True};method='explicit conjunction truth cases plus physical-profile preservation'
        elif cid=='AEX-07-R01':ok=reference_ok and len(ids['AEX-07'])==67;evidence={'allRecipeIds':ids['AEX-07']}
        elif cid=='AEX-07-R02':ok=locator_ok and len(public)==100;evidence={'allResolvedPublicCodes':sorted(public_codes),'publicEnvelopeValidatorChecks':1725}
        else:
            text,terms=requirements[cid];missing=[t for t in terms if t not in text];ok=not missing
            evidence={'requiredClauses':terms,'missing':missing,'evidenceTextSha256':hashlib.sha256(text.encode()).hexdigest()}
        focused.append({**case,'status':'PASS authored correction gate' if ok else 'FAIL','pass':ok,'method':method,'evidence':evidence,'authoredAdjudication':case['expected'],'advancedRuntimeExecuted':False})
    assert len(focused)==specs['caseCount']==33
    protected=read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes']
    check('protected-inputs',len(protected)==138 and all(sha(G/f)==h for f,h in protected.items()))
    artifactpaths=[ip,pp,R/d['sharedGuide'],R/d['bodyGuide'],R/p['guide'],R/p['bodyGuide']]
    for trade in ['ENCHANTING','RUNE_CARVING','SCRIBING','TINKERING']:
        artifactpaths += [R/f'docs/director-only/{trade}_INTERNAL_RECIPE_CARDS.md',R/f'docs/mechanics/{trade}_CANDIDATE_RECIPE_CARDS.md']
    for path in artifactpaths[6:]:
        audience=cards if 'director-only' in str(path) else public
        trade=path.name.split('_INTERNAL_')[0].split('_CANDIDATE_')[0].replace('_',' ').title()
        check(rel(path)+'-complete-cards',all(c['manuscriptText'] in path.read_text(encoding='utf-8') for c in audience.values() if c['sourceRecipe']['skill']==trade))
    failed=[c for c in allchecks+focused if not c['pass']]
    report={'status':'PASS' if not failed else 'FAIL','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'completionGateSatisfied':not failed,'conditionsSatisfied':list(ids) if not failed else [],'scope':'Current full-cohort textual/source/numeric preservation plus 33 finite authored adjudications; no advanced runtime, actual-world, human balance or whole-game approval.','verdictFile':rel(V/reg['verdictFile']),'verdictSha256':reg['verdictSha256'],'reviewerSpecificationsSha256':sha(V/'AEX_167_FOCUSED_REGRESSIONS.json'),'validatorSha256':sha(Path(__file__)),'artifactHashes':{rel(f):sha(f) for f in artifactpaths},'existingSuites':existing,'existingChecks':sum(x['checks'] for x in existing),'focusedCases':33,'staticChecks':len(allchecks),'checks':allchecks,'focusedAdjudications':focused,'failed':failed,'protectedInputsUnchanged':138 if not failed else None,'recipesPromoted':0,'runtimeImplemented':False,'balanceApproved':False}
    dump(A/'ADVANCED_167_EXACT_COMPLETION_VALIDATION.json',report)
    print(json.dumps({k:report[k] for k in ['status','completionGateSatisfied','existingChecks','focusedCases','staticChecks','failed']},ensure_ascii=False,indent=2))
    if failed:raise SystemExit(1)

if __name__=='__main__':main()
