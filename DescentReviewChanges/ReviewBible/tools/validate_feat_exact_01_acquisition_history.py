"""Independent hand-authored acquisition/history boundary vectors.

These checks do not synthesize fully qualified campaign characters from the
335 prerequisite trees. Tests of paid identities explicitly supply prerequisite
truth; numeric gates, history, schedules and fixed branches have separate scope.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from copy import deepcopy
import json
import argparse
import feat_exact_01_acquisition_models as m

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def normalized(x):
    if isinstance(x,set):return sorted(x)
    if isinstance(x,tuple):return list(x)
    return x

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report',type=Path,default=A/'FEAT_EXACT_01_ACQUISITION_HISTORY_CHECK.json')
    parser.add_argument('--source-descendants', type=Path, action='append', default=[])
    args=parser.parse_args()
    if args.report.exists():raise SystemExit('Preserve old report; use a fresh --report path.')
    contracts=read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json');cr={x['id']:x for x in contracts['records']}
    public=read(R/'data/public/feat_candidates/exact_01/candidate.json');pr={x['id']:x for x in public['feats']}
    class_paths={n:R/f'data/public/class_playtests/{n.lower()}.json' for n in ['Warrior','Mage','Soldier','Oracle']}
    classes={n:read(p) for n,p in class_paths.items()};schedules={n:d['asiClassLevels'] for n,d in classes.items()}
    warrior_cards={x['id']:x for x in classes['Warrior']['cards']}
    hm=read(R/'data/director/feat_candidates/exact_01/cohorts/heritage_mutation.json')
    pairs={x['completeClassCounterpart']['id']:x['featId'] for x in hm['originalWarriorCounterpartPairs']}
    supp=read(R/'data/public/feat_candidates/exact_01/supplements.json')
    curricula=set(next(x['value'] for x in supp['groups'] if x['id']=='SUP-04'))
    scores={'STR':13,'DEX':13,'CON':13,'INT':13,'WIS':13,'CHA':13}
    checks=[]
    def check(name,actual,expected,kind='bounded-reference'):
        a,e=normalized(deepcopy(actual)),normalized(deepcopy(expected));checks.append({'name':name,'kind':kind,'actual':a,'expected':e,'pass':a==e})
    def reject(name,fn):
        try:fn()
        except ValueError as err:check(name,'rejected','rejected');checks[-1]['reason']=str(err)
        else:check(name,'accepted','rejected')
    def actor(name='Soldier',level=20):
        return m.PaidChoices(schedules,pairs,{name:level},deepcopy(scores),set(cr),available_curricula=curricula)
    def earn(a,name,level):
        key=f'{name}:{level}';a.earn_class_opportunity(key,name,level);return key

    binding_resolutions=[]
    declared_changes=[]
    for receipt_path in args.source_descendants:
        for change in read(receipt_path)['changes']:
            declared_changes.append({**change, 'receipt': info(receipt_path)})
    for b in contracts['sourceBindings']:
        expected=deepcopy(b); actual=info(G/b['path']); chain=[]; visited=set()
        while expected != actual:
            if expected['sha256'] in visited:
                raise AssertionError('Cyclic source-binding history: '+b['path'])
            visited.add(expected['sha256'])
            matches=[c for c in declared_changes if c['before']['path']==b['path']
                     and c['after']['path']==b['path'] and c['before']['sha256']==expected['sha256']
                     and c['before']['bytes']==expected['bytes']]
            if len(matches)!=1:
                raise AssertionError('Missing or ambiguous explicit descendant: '+b['path'])
            change=matches[0]; preserved=info(G/change['before']['preservedCopy'])
            if preserved['bytes']!=expected['bytes'] or preserved['sha256']!=expected['sha256']:
                raise AssertionError('Preserved before-version mismatch: '+b['path'])
            expected=deepcopy(change['after']); chain.append(deepcopy(change))
        check('Bound contract source '+b['path'],actual,expected,'input-integrity')
        binding_resolutions.append({'originalContractBinding':deepcopy(b), 'actualCurrentBinding':actual, 'explicitDescendantChain':chain})
    check('All335 IDs exact order',[x['id'] for x in contracts['records']],[x['id'] for x in public['feats']],'source-integrity')
    for sid,c in cr.items():
        check(sid+' full original object',c['originalObject'],pr[sid]['sourceObject'],'source-integrity')
        # Full text checked without flooding report with duplicate entire procedures.
        proc=pr[sid].get('operationalRules') or pr[sid]['unchangedReviewedRecord']['operationalRules']
        check(sid+' complete operative procedure',c['completeOperativeProcedure']==proc,True,'source-integrity')
    for sid in [x for x in pr if 'unchangedReviewedRecord' in pr[x]]:
        check(sid+' reviewed envelope untouched',cr[sid]['unchangedReviewedEnvelope']==pr[sid]['unchangedReviewedRecord'],True,'source-integrity')

    check('Oracle actual schedule',schedules['Oracle'],[4,8,14,19],'source-data')
    check('Warrior actual schedule',schedules['Warrior'],[4,8,12,16,19],'source-data')
    a=actor('Oracle',12)
    reject('Total/Oracle12 does not invent Oracle ASI12',lambda:earn(a,'Oracle',12))
    reject('Oracle12 has not reached actual Oracle14 grant',lambda:earn(a,'Oracle',14))
    a.current_classes['Oracle']=14;check('Actual Oracle14 grant can be recorded',earn(a,'Oracle',14),'Oracle:14')
    reject('Same earned grant cannot get new identity',lambda:a.earn_class_opportunity('renamed','Oracle',14))
    a=actor('Soldier',3);a.current_classes['Mage']=1
    reject('Total4 with Soldier3/Mage1 grants neither class4 ASI',lambda:earn(a,'Soldier',4))
    reject('Meeting prerequisite alone does not supply feat choice',lambda:a.commit('alert','unearned',prerequisites_met=True))
    a=actor();op=earn(a,'Soldier',4)
    reject('Actual choice still requires prerequisites',lambda:a.commit('alert',op,prerequisites_met=False))
    check('Rejected unmet-prerequisite attempt preserves choice',a.opportunities[op]['spent'],False)
    a.commit('alert',op,prerequisites_met=True)
    reject('One opportunity cannot pay two feats',lambda:a.commit('alertness',op,prerequisites_met=True))
    op2=earn(a,'Soldier',8)
    reject('Nonrepeatable feat cannot reacquire',lambda:a.commit('alert',op2,prerequisites_met=True))
    a.suppress('alert');reject('Suppression does not erase paid identity',lambda:a.commit('alert',op2,prerequisites_met=True));a.suppress('alert',False)
    check('Restoration keeps one identity',len(a.grants),1)

    for source_id,feat_id in pairs.items():
        a=actor('Warrior',20);one=earn(a,'Warrior',16);two=earn(a,'Warrior',19)
        # Each fixture tests paid identity only, after an independently established prerequisite receipt.
        a.commit(source_id,one,prerequisites_met=True)
        reject(feat_id+' cannot pay again through feat spelling',lambda sid=feat_id,op=two:a.commit(sid,op,prerequisites_met=True))
        check(feat_id+' current class counterpart preserved',cr[feat_id]['sharedPaidIdentity']['completeClassCounterpart']==warrior_cards[source_id],True,'source-data')
        check(feat_id+' actual Warrior class minimum carried forward',cr[feat_id]['requirements']['requirements'][0],
              {'kind':'classLevel','className':'Warrior','minimum':warrior_cards[source_id]['minimumClassLevel']},'source-data')
        check(feat_id+' one spent opportunity only',sum(x['spent'] for x in a.opportunities.values()),1)
    check('Exactly12 explicit shared mutation identities',len(pairs),12,'source-data')
    a=actor();actual_mage_ids={x['id'] for x in classes['Mage']['cards']}
    check('Real similarly named class card exists','mage.base.elemental-affinity' in actual_mage_ids,True,'source-data')
    check('Unmapped actual class identity does not alias feat',a.canonical('mage.base.elemental-affinity'),'mage.base.elemental-affinity')
    reject('Feat opportunity cannot buy similarly named class card',lambda:a.commit('mage.base.elemental-affinity',earn(a,'Soldier',8),prerequisites_met=True))
    a.commit('elemental_affinity','Soldier:8',prerequisites_met=True)
    check('Actual separate feat identity remains available',a.has('elemental_affinity'),True)

    a=actor();a.scores['STR']=19
    reject('PureASI cannot waste second point at19',lambda:a.commit('abilityScoreImprovement',earn(a,'Soldier',4),{'STR':2},True))
    check('Rejected allocation leaves opportunity unspent',a.opportunities['Soldier:4']['spent'],False)
    a.commit('abilityScoreImprovement','Soldier:4',{'STR':1,'DEX':1},True)
    check('Full split allocation',[a.scores['STR'],a.scores['DEX']],[20,14])
    a.commit('abilityScoreImprovement',earn(a,'Soldier',8),{'DEX':2},True)
    check('RepeatASI requires another opportunity',a.scores['DEX'],16)
    op=earn(a,'Soldier',12)
    reject('PureASI cannot bank one point',lambda:a.commit('abilityScoreImprovement',op,{'INT':1},True))
    reject('PureASI cannot allocate three points',lambda:a.commit('abilityScoreImprovement',op,{'INT':2,'WIS':1},True))
    a=actor();a.commit('armorProficiency',earn(a,'Soldier',4),'heavy',True)
    check('Direct heavy proficiency grants only heavy',a.armor_proficiencies,{'heavy'})
    op=earn(a,'Soldier',8);reject('Already proficient tier is invalid',lambda:a.commit('armorProficiency',op,'heavy',True))
    a.commit('armorProficiency',op,'light',True);check('Different missing tier allowed',a.armor_proficiencies,{'heavy','light'})
    a=actor();a.scores['CON']=21
    a.commit('resilient',earn(a,'Soldier',4),'CON',True)
    check('Half-feat ceiling never reduces score21',[a.scores['CON'],a.save_proficiencies],[21,{'CON'}])
    op=earn(a,'Soldier',8);reject('Resilient same save cannot repeat',lambda:a.commit('resilient',op,'CON',True))
    a.commit('resilient',op,'WIS',True);check('Different save repeat legal',a.scores['WIS'],14)
    a=actor();a.weapon_proficiencies={'longsword','shortbow'}
    a.commit('weaponFocus',earn(a,'Soldier',4),'longsword',True)
    op=earn(a,'Soldier',8);reject('Same weapon Focus cannot repeat',lambda:a.commit('weaponFocus',op,'longsword',True))
    reject('Unproficient weapon not an eligible choice',lambda:a.commit('weaponFocus',op,'whip',True))
    a.commit('weaponFocus',op,'shortbow',True)
    check('Two different weapon choices share family but not profile',len(a.grants),2)
    a.weapon_proficiencies.remove('longsword')
    check('Proficiency loss disables use without deleting grant',[a.weapon_focus_operative('longsword'),a.has('weaponFocus')],[False,True])
    a.weapon_proficiencies.add('longsword');check('Real restoration restores same bonus',a.weapon_focus_operative('longsword'),True)

    a=actor();a.commit('magicInitiate',earn(a,'Soldier',4),{'curriculum':'Wizard'},True)
    op=earn(a,'Soldier',8);reject('NamedWizard cannot duplicate genericWizard',lambda:a.commit('magic_initiate_wizard',op,None,True))
    a.commit('magic_initiate_bard',op,None,True)
    check('Distinct named curriculum can coexist',[x.get('curriculum') for x in a.grants],['Wizard','Bard'])
    reject('Generic identity itself remains nonrepeatable',lambda:a.commit('magicInitiate',earn(a,'Soldier',12),{'curriculum':'Cleric'},True))
    a=actor();a.commit('magic_initiate_wizard',earn(a,'Soldier',4),None,True)
    reject('GenericWizard cannot duplicate namedWizard',lambda:a.commit('magicInitiate',earn(a,'Soldier',8),{'curriculum':'Wizard'},True))
    reject('Unlisted curriculum not supplied by generic name',lambda:a.commit('magicInitiate','Soldier:8',{'curriculum':'Invented Class'},True))

    expected_training={
      'athleticProdigy':(['Athletics','Acrobatics'],True),'charismatic':(['Persuasion','Deception'],True),
      'diplomat':(['Persuasion','Insight'],True),'naturalist':(['Nature','Survival'],True),
      'acrobatic':(['Acrobatics'],False),'ranger_training':(['Survival','Nature'],False)}
    for sid,(skills,branching) in expected_training.items():
        rules=cr[sid]['fixedTrainingBranches'];check(sid+' exact skill recipients',list(rules),skills,'source-data')
        for before,expected in [(0,1),(1,2 if branching else 1),(2,2 if branching else 1)]:
            t=m.FixedTraining();got=t.acquire(sid,rules,{s:before for s in skills})
            check(sid+f' fixed branch from proficiency{before}',got,{s:expected for s in skills})
            reject(sid+f' branch cannot be reacquired from{before}',lambda:t.acquire(sid,rules,{s:1 for s in skills}))
            t.suppressed.add(sid);check(sid+' independent proficiency while suppressed',t.contribution(sid,skills[0],1),1)
            t.suppressed.clear();check(sid+' original branch restored',t.contribution(sid,skills[0],1),max(expected,1))
        t=m.FixedTraining();t.acquire(sid,rules,{skills[0]:0})
        check(sid+' later proficiency is not automatic Expertise',t.contribution(sid,skills[0],1),1)
        check(sid+' independent Expertise is strongest, not4PB',t.contribution(sid,skills[0],2),2)
    t=m.FixedTraining();rules=cr['naturalist']['fixedTrainingBranches']
    check('Two skill snapshots evaluated independently',t.acquire('naturalist',rules,{'Nature':1,'Survival':0}),{'Nature':2,'Survival':1})

    for permanent,threshold,temporary,expected in [(12,13,5,False),(13,13,0,True),(14,15,10,False),(15,15,0,True),(16,17,4,False),(17,17,0,True)]:
        check(f'Permanent ability{permanent} gate{threshold} temp{temporary}',m.ability_gate(permanent,threshold,temporary),expected)
    for score,total,contribution,expected in [(14,4,1,4),(13,4,1,3),(14,5,1,5),(12,4,2,5),(14,4,2,6),(10,17,1,6)]:
        check(f'Permanent skill score{score} level{total} factor{contribution}',m.permanent_skill_modifier(score,total,contribution),expected)
    reject('Untrained ability total cannot satisfy numerical skill gate',lambda:m.permanent_skill_modifier(20,20,0))
    reject('Expertise never becomes4PB',lambda:m.permanent_skill_modifier(14,4,4))
    check('Thievery bridge uses DEX/tool permanent total',cr['lock_savant']['requirements']['requirements'][1]['ability'],'DEX','source-data')
    check('Tinkering5 is trained trade level, not INT+PB',cr['tinker_adept']['requirements'],{'kind':'trainedTradeLevel','trade':'Tinkering','minimum':5,'notSkillCheckBonus':True},'source-data')

    use=m.FiniteFeatUse(3,3);use.spend(2);use.operative=False
    reject('Suppressed Lucky cannot spend',lambda:use.spend())
    check('Suppression preserves one remaining point',use.current,1)
    use.operative=True;reject('Reacquisition cannot initialize again',use.reacquire)
    check('Debt-only rest no refill',use.rest('debt',False),False)
    check('Actual beneficial rest refills',use.rest('beneficial-LR',True),True)
    use.spend();check('Same rest cannot be replayed',use.rest('beneficial-LR',True),False)
    check('Replayed rest leaves spent use spent',use.current,2)
    capacity=m.FiniteFeatUse(2,1);capacity.capacity(3)
    check('PB-capacity growth no refill',[capacity.maximum,capacity.current],[3,1])
    reserve=m.FiniteFeatUse(10,0);check('Explicit empty reserve remains empty on acquisition',reserve.current,0)
    base=m.VisionChoice.acquire([]);ext=m.VisionChoice.acquire([60])
    check('No prior vision fixes base60',base.current([]),60)
    check('Existing60 fixes extension30',ext.current([60]),90)
    check('Suppressed underlying vision does not create fallback60',ext.current([]),0)
    check('Later stronger actual base receives same extension',ext.current([60,120]),150)
    ext.operative=False;check('Suppressed feat leaves independent base',ext.current([60]),60)
    ext.operative=True;check('Restoration keeps original branch',ext.current([60]),90)
    check('Base branch never becomes later extension',base.current([120]),120)

    failures=[x for x in checks if not x['pass']]
    paths=[Path(__file__),R/'tools/feat_exact_01_acquisition_models.py',A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
           R/'data/public/feat_candidates/exact_01/candidate.json',R/'data/public/feat_candidates/exact_01/supplements.json',
           R/'data/director/feat_candidates/exact_01/cohorts/heritage_mutation.json',*class_paths.values(),*args.source_descendants]
    result={'createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass' if not failures else 'fail',
      'scope':'Acquisition-history/identity, class schedules, repeatable choices, six fixed training entries, numeric permanent gates, finite uses and fixed vision. Not complete335-character premise validation.',
      'sourceBindings':[info(p) for p in paths],'historicalContractBindingResolutions':binding_resolutions,
      'checks':len(checks),'checkKinds':{k:sum(x['kind']==k for x in checks) for k in sorted({x['kind'] for x in checks})},
      'failureCount':len(failures),'failures':failures,'results':checks,
      'all335PrerequisiteContractsNormalized':True,'all335ActualAcquisitionBoundaryCasesExecuted':False,'fullFeatRuntimeCases':0,
      'doesNotAuthenticatePrerequisiteReceipts':True,'remaining':['Audit all175 gate forms with source-qualified positive/negative actor histories, especially AND/OR branches and absent legacy receipts.',
      'Carry forward actual GPT FEAT327-ACQ-01 and its separate derived-correction receipt; it does not close all prerequisite cases.',
      'Dragon Blood normalized contract now requires its actual recorded ancestry damage type on either branch; authenticate the receipt in each actual fixture.',
      'Recheck all explicit per-feat acquisition choices against finite supplement tables; no generic prerequisite success grants runtime use.',
      'Continue full FXC-04–10 and manifest-bound exact GPT submission; no premature catalog promotion.'],
      'candidateReadyForSubmission':False,'exactApproved':False,'sourceInformationDeleted':0}
    args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=normalized)+'\n',encoding='utf-8')
    print(json.dumps({'report':info(args.report),'checks':len(checks),'kinds':result['checkKinds'],'failures':len(failures),
      'failedNames':[x['name'] for x in failures],'all335ActualAcquisitionBoundaryCasesExecuted':False}))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
