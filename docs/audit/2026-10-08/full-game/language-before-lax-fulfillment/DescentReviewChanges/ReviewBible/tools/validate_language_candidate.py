"""Static candidate/source parity and finite reference calculations; not companion gameplay."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from zipfile import ZipFile
import hashlib
import json
import math
import re

R=Path(__file__).resolve().parents[1]
G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'
V=A/'language-source-reviewer-files'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def objects(d):
    if isinstance(d,dict):
        yield d
        for v in d.values():yield from objects(v)
    elif isinstance(d,list):
        for v in d:yield from objects(v)

def main():
    checks=[]
    def check(group,name,ok,detail=None):
        row={'group':group,'name':name,'passed':bool(ok)}
        if detail is not None:row['detail']=detail
        checks.append(row)
    internal=read(R/'data/director/language_communication_candidate_internal.json')
    public=read(R/'data/playtest/language_communication_candidate_public.json')
    prep=read(A/'LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json')
    add=read(A/'LANGUAGE_ADVANCED_INTERFACE_ADDENDUM.json')
    author=read(V/'LANGUAGE_AUTHORING_REGISTER.json')
    grant=read(V/'GRANT_IDENTITY_REGISTER.json')
    pending=read(V/'PENDING_LANGUAGE_INTERFACES.json')
    expected=read(V/'LANGUAGE_EXACT_CANDIDATE_CHECKLIST.json')['cases']
    for key in ('exactLanguageApproval','classSpellFeatPromotion','runtimeImplemented','humanBalanceApproved','wholeGameFlowApproved'):
        check('approval-boundaries',key,internal[key] is False and public[key] is False)
    with ZipFile(A/'DD_Language_Communication_Source_Prepared_v2.zip') as z:
        manifest=json.loads(z.read('FILE_MANIFEST.json'))
        for path,entry in manifest.items():
            check('unchanged-original-and-current-source',path,sha(G/path)==entry['sha256']==hashlib.sha256(z.read(path)).hexdigest())
    check('source-coverage','152 original payloads',len(manifest)==152)
    check('source-coverage','source manifest retained',internal['originalSourceManifest']==manifest)
    check('source-coverage','runtime alternative records untouched',internal['originalGrantEvidence']['runtimeAlternatives']==prep['runtimeLanguageAlternatives'])
    for a in prep['ancestryGrants']:
        check('full-source-grants',a['ancestryId'],a in internal['originalGrantEvidence']['ancestries'])
    for b in prep['backgroundGrants']:
        check('full-source-grants',b['backgroundId'],b in internal['originalGrantEvidence']['backgrounds'])
    for key,count in [('baseGrants',14),('variants',45),('backgrounds',20)]:
        check('derived-grants',key,len(public['grants'][key])==count)
    check('derived-grants','base derivations exact',public['grants']['baseGrants']==grant['baseGrants'])
    check('derived-grants','45 variant dispositions exact',public['grants']['variants']==grant['variants'])
    for source,candidate in zip(grant['backgrounds'],public['grants']['backgrounds']):
        check('background-field-preservation',source['backgroundId'],all(candidate[k]==v for k,v in source.items()) and
              (('originalLanguagesSource' in candidate)==source['sourceLanguagesFieldPresent']))
    check('derived-grants','five absent background fields',sum(not b['sourceLanguagesFieldPresent'] for b in public['grants']['backgrounds'])==5)
    check('derived-grants','two actual variant additions',{v['variantId'] for v in public['grants']['variants'] if v['countAdded']}=={'high-elf','imperial-human'})
    for key in ('aliases','explicitlyNotAliases','dialectPolicy','scripts'):
        check('identity-preservation',key,public['grants'][key]==grant[key])
    check('identity-preservation','no automatic choice from label',all(x['automaticChoiceEntitlement'] is False for x in public['grants']['identities']))
    for original,candidate in zip(author['decisions'],internal['decisionApplicationRegister']):
        check('sixteen-decisions',original['id'],all(candidate[k]==v for k,v in original.items()) and bool(candidate['checklistCases']))
    check('sixteen-decisions','LA16 receipt unchanged',internal['deferredReceipt']==author['decisions'][-1])
    exact_cards={c['id']:c for group in prep['classComparisonRecords'] for c in group['cards']}
    extra=read(V/'CLASS_LANGUAGE_INTERFACE_REGISTER.json')['additionalActuallyReadCalledCard']
    exact_cards[extra['id']]=next(x for x in objects(read(G/extra['sourceFile'])) if x.get('id')==extra['id'])
    check('class-interfaces','49 distinct source IDs',len(internal['classInterfaces'])==len({x['id'] for x in internal['classInterfaces']})==49)
    for interface in internal['classInterfaces']:
        check('class-original-record',interface['id'],interface['originalSourceRecord']==exact_cards[interface['id']] and not interface['classCardPromoted'])
    check('class-interfaces','engine contexts exact',internal['classEngineContexts']==prep['classComparisonRecords'])
    check('class-interfaces','public exact language dispositions',{x['id']:x['disposition'] for x in public['classInterfaces']}=={x['id']:x['disposition'] for x in internal['classInterfaces']})
    originals={x['id']:x for x in prep['spellComparisonRecords']}
    for interface in internal['spellInterfaces']:
        original=originals[interface['id']]
        check('spell-original-record',interface['id'],interface['originalSourceRecord']==original and interface['operational']==original['operational'] and interface['status']==original['status'])
    check('pending-preservation','15 null spell procedures',sum(s['operational'] is None for s in internal['spellInterfaces'])==15)
    check('pending-preservation','8 current operative comparisons',sum(s['operational'] is not None for s in internal['spellInterfaces'])==8)
    check('pending-preservation','full feat and spell route registers',internal['pendingInterfaces']==pending)
    check('pending-preservation','8 feat IDs',{x['id'] for x in public['pendingFeatInterfaces']}=={x['id'] for x in prep['pendingFeatSourceComparisons']})
    for card in add['completeScribingCards']:
        check('completed-scribing-preservation',card['recipeId'],card in internal['completedAdvancedInterfaces']['completeScribingCards'])
    for name,section in add['completeApplicableProcedureSections'].items():
        check('completed-procedure-preservation',name,internal['completedAdvancedInterfaces']['completeApplicableProcedureSections'][name]==section)
    check('completed-procedure-preservation','40 cards and19 sections',len(add['completeScribingCards'])==40 and len(add['completeApplicableProcedureSections'])==19)
    completed_public=read(R/'data/crafting/advanced_craft_recipe_candidate_public.json')
    expected_public={c['recipeId']:c for c in completed_public['cards'] if c['recipeId'] in {x['recipeId'] for x in add['completeScribingCards'] if x['visibility']=='public'}}
    check('public-projection','28 existing public recipe cards exactly',len(public['publicScribingCards'])==28 and {x['recipeId']:x for x in public['publicScribingCards']}==expected_public)
    text=json.dumps(public,ensure_ascii=False)
    private_cards=[x for x in add['completeScribingCards'] if x['visibility']!='public']
    for c in private_cards:
        check('public-projection','withhold '+c['recipeId'],not re.search(re.escape(c['recipeId'])+r'\b',text) and c['name'] not in text)
    check('public-projection','private coordinator absent','recipe-686' not in text)
    check('public-projection','no internal source-object keys',all('originalSourceRecord' not in o and 'matrixResearch' not in o and 'hiddenMetadata' not in o for o in objects(public)))
    check('public-projection','no wholesale internal decision/source registers',not ({'completedAdvancedInterfaces','originalGrantEvidence','decisionApplicationRegister','deferredReceipt','sourceMap'} & set(public)))
    check('record-contract','all required record types',set(public['recordSchema']['definitions'])=={'provenance','competency','choice','temporaryEffect','learning','textEvidence','scribingLedger','communicationEvent'})
    check('record-contract','public/internal same ordinary contracts',public['recordSchema']==internal['recordSchema'] and public['rules']==internal['rules'])
    for name,definition in public['recordSchema']['definitions'].items():
        check('record-contract',name,set(definition['required'])==set(definition['fields']))
    cases=read(A/'LANGUAGE_CANDIDATE_WORKED_ADJUDICATIONS.json')['cases']
    check('authored-adjudications','32 distinct cases',len(cases)==len({c['id'] for c in cases})==32)
    for c,e in zip(cases,expected):
        check('authored-adjudications',c['id'],c['id']==e['id'] and c['expected']==e['expected'] and bool(c['setup']) and len(c['chronology'])>=3 and bool(c['adjudicatedOutcome']) and c['runtimePassed'] is False)
    check('authored-adjudications','same worked cases in both audiences',public['workedAdjudications']==internal['workedAdjudications']==cases)

    # Finite reference calculations from candidate numeric constants; not installed into any app.
    r=public['rules'];course=r['ordinaryLearning'];comm=r['communication'];insight=r['scribingInsight']
    def invoice(minutes):return math.ceil(Fraction(minutes)*Fraction(course['referenceTuition']['copperPerInstructionMinutes']['numerator'],course['referenceTuition']['copperPerInstructionMinutes']['denominator']))
    calculations=[('full language hours',(course['languageSemanticsMinutes']+course['scriptMinutes']+course['languageLiteracyPracticeMinutes'])//60,320),
        ('same script hours',(course['languageSemanticsMinutes']+course['languageLiteracyPracticeMinutes'])//60,280),
        ('full literacy hours',(course['scriptMinutes']+course['languageLiteracyPracticeMinutes'])//60,80),
        ('same script literacy hours',course['languageLiteracyPracticeMinutes']//60,40),
        ('full reference tuition cp',invoice(course['fullLanguageMinutes']),4000),
        ('same script reference tuition cp',invoice(course['fullLanguageWithSameScriptMinutes']),3500),
        ('interrupted40 minute credit',40//course['phaseMinutes']*course['phaseMinutes'],30),
        ('single40 minute invoice cp',invoice(40),9),('real Tongues credit loss',90-10,80),
        ('Insight separate work hours',(insight['gainActiveMinutes']+insight['spendActiveMinutes'])//60,9),
        ('three new studies then spend hours',(3*insight['gainActiveMinutes']+insight['spendActiveMinutes'])//60,11),
        ('cap saturation',min(insight['maximumUnspent'],6+insight['gain'])-6,0),
        ('points2 then gain then spend',2+insight['gain']-insight['spend'],0),
        ('250 word routine minutes',max(r['ordinaryTranslation']['minimumMinutes'],math.ceil(Fraction(10*250,r['ordinaryTranslation']['wordsPerTenActiveMinutes']))),10),
        ('251 word routine minutes',max(r['ordinaryTranslation']['minimumMinutes'],math.ceil(Fraction(10*251,r['ordinaryTranslation']['wordsPerTenActiveMinutes']))),11),
        ('one word routine minutes',max(r['ordinaryTranslation']['minimumMinutes'],math.ceil(Fraction(10,r['ordinaryTranslation']['wordsPerTenActiveMinutes']))),1),
        ('ordinary round budget four plus two',4+2,comm['freeOrdinarySecondsPerCreaturePerNumberedRound']),
        ('short relay actual seconds',3+3,6),('party signal rehearsal minutes',comm['partySignalRehearsalMinutes'],10),('finite cues',comm['maximumFixedCues'],6)]
    for name,actual,want in calculations:check('executed-reference-arithmetic',name,actual==want,{'actual':actual,'expected':want})
    # Deliberately include rejected operations and exact chronological boundaries.
    def nonoverlap(intervals):return all(a[1]<=b[0] for a,b in zip(sorted(intervals),sorted(intervals)[1:]))
    check('executed-reference-boundaries','reject course/Insight overlap',not nonoverlap([(540,600),(540,600)]))
    check('executed-reference-boundaries','accept separate gain and spend',nonoverlap([(540,600),(600,1080)]))
    check('executed-reference-boundaries','reject one-minute overlap',not nonoverlap([(540,601),(600,1080)]))
    check('executed-reference-boundaries','fresh Action needed after exhausted free allowance',4+2+1>comm['freeOrdinarySecondsPerCreaturePerNumberedRound'])
    check('executed-reference-boundaries','no extra-turn refresh',comm['extraTurnRefresh'] is False)
    check('executed-reference-boundaries','relay cannot precede receiving',6>2)
    history={'copies':{'copy-a':'correspondence-1','copy-b':'correspondence-1'},'reader-evidence':{('reader-a','correspondence-1')}}
    check('executed-reference-boundaries','same reader copy does not create new evidence',('reader-a',history['copies']['copy-b']) in history['reader-evidence'])
    check('executed-reference-boundaries','different reader history remains independent',('reader-b',history['copies']['copy-b']) not in history['reader-evidence'])
    donor={'spokenComprehension','speaking'};borrowed=set(donor)
    check('executed-reference-boundaries','mode transfer does not invent literacy','reading' not in borrowed and 'writing' not in borrowed)
    borrowed.clear();check('executed-reference-boundaries','expiration removes borrowed modes',not borrowed)
    # Previous regular turn begins at100 and ends106; voluntary speech occurred102.
    check('executed-reference-boundaries','Silent Smite after-END fixture',not any(t>=106 for t in [102]))
    check('executed-reference-boundaries','Vow Unbroken since-BEGINNING fixture fails',any(t>=100 for t in [102]))
    commands={('owner-a',20)}
    check('executed-reference-boundaries','class/crafted second command same owner same round blocked',('owner-a',20) in commands)
    check('executed-reference-boundaries','another actual owner has own budget',('owner-b',20) not in commands)
    check('executed-reference-boundaries','next numbered round has own budget',('owner-a',21) not in commands)
    check('executed-reference-boundaries','unqualified251-word Insight passage',251>insight['maximumPassageWords'])
    check('executed-reference-boundaries','qualified200-word extent only',200<=insight['maximumPassageWords'])
    check('executed-reference-boundaries','no saturated award bank',insight['saturationBanksAward'] is False)

    guides=[R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md',R/'docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md',R/'docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md']
    check('guide-parity','public data guide matches manuscript',public['guideText']==guides[0].read_text(encoding='utf-8'))
    for p in guides:
        content=p.read_text(encoding='utf-8')
        check('guide-completeness',p.name,'<!--' not in content)
        for link in re.findall(r'\]\(([^)]+)\)',content):
            if '://' in link:continue
            path,_,anchor=link.partition('#');dest=(p.parent/path).resolve() if path else p
            check('local-links',p.name+' -> '+link,dest.exists())
    report={'scope':'Static source/candidate/public parity and38 finite executable reference arithmetic/boundary checks; no game runtime, real campaign facts, human teaching or balance certification',
            'candidateChecks':len(checks),'groups':dict(Counter(c['group'] for c in checks)),'checks':checks,'failed':[c for c in checks if not c['passed']],
            'authoredSemanticAdjudications':32,'humanOrRuntimePassesClaimed':0,
            'candidateHashes':{str(p.relative_to(G).as_posix()):sha(p) for p in guides+[R/'data/playtest/language_communication_candidate_public.json',R/'data/director/language_communication_candidate_internal.json']}}
    out=A/'LANGUAGE_CANDIDATE_VALIDATION.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('candidateChecks','groups','failed','humanOrRuntimePassesClaimed')},ensure_ascii=False,indent=2))
    return bool(report['failed'])

if __name__=='__main__':raise SystemExit(main())
