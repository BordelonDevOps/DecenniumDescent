"""Apply only the actual GPT FEAT327-ACQ-01 finite source correction.

Original source package is immutable. This creates measured descendants and
retains source-directed acquisition predicates; it grants no exact approval.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from copy import deepcopy
import json
import re

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
I=R/'data/director/feat_candidates/exact_01';U=R/'data/public/feat_candidates/exact_01';D=R/'docs/feats/exact-candidate-01'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def at(d,p):
    for k in p.strip('/').split('/'):d=d[int(k)] if isinstance(d,list) else d[k]
    return d
def put(d,p,v):
    parts=p.strip('/').split('/');parent=d
    for k in parts[:-1]:parent=parent[k]
    parent[parts[-1]]=v

def main():
    receipt=A/'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json';assert not receipt.exists()
    source=read(A/'FEAT327_ACQ_01_GPT_RESPONSE.json');answer=source['fullResponse']
    assert source['replyId']=='70d1835d-4e41-41dd-9646-d07e22e442cc' and source['status']=='completed'
    paragraph=next(x[2:] for x in answer.splitlines() if x.startswith('> **Weapon prerequisite bridge.**'))
    suffix=next(x[2:] for x in answer.splitlines() if x.startswith('> For weapon prerequisites, apply FS-02'))
    anchor='Existing genuinely authorized legacy grants remain evidenced; no new builder option follows.'
    snapshot=read(A/'feat-exact-01-before-acq01/PRESERVATION_MANIFEST.json')
    for rel,b in snapshot.items():
        saved=G/b['preservedCopy'];assert info(saved)['sha256']==b['sha256']
    # Scripts were separately corrected after preserving their unexecuted/current predecessors.
    outputs=[I/'shared_rules.json',U/'shared_rules.json',D/'SHARED_RULES.md',I/'convention_dispositions.json']
    outputs += [I/f'cohorts/{c}.json' for c in ['combat','general_combat','heritage_mutation']]
    outputs += [A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md']
    for p in outputs:assert info(p)['sha256']==snapshot[p.relative_to(G).as_posix()]['sha256']
    operations=[]
    for p in [I/'shared_rules.json',U/'shared_rules.json']:
        d=read(p);assert d['rules'][1]['id']=='FS-02';old=d['rules'][1]['wording'];assert old.count(anchor)==1
        new=old.replace(anchor,anchor+'\n\n'+paragraph);d['rules'][1]['wording']=new
        operations.append({'file':p.relative_to(G).as_posix(),'pointer':'/rules/1/wording','old':old,'new':new,'authority':'FEAT327-ACQ-01/ACQ-01.1'})
        write(p,d)
    p=D/'SHARED_RULES.md';s=p.read_text('utf-8');assert s.count(anchor)==1
    p.write_text(s.replace(anchor,anchor+'\n\n'+paragraph),encoding='utf-8')
    conv=read(I/'convention_dispositions.json')
    selected={35:('combat','/sharedProposal/Authority and acquisition'),42:('general_combat','/sharedProposal/Authority and acquisition'),
              50:('general_combat','/proposedCombatConventionDependency/Authority and acquisition'),84:('heritage_mutation','/proposedCombatDependency/Authority and acquisition')}
    cohorts={c:read(I/f'cohorts/{c}.json') for c in {x[0] for x in selected.values()}}
    for index,(cohort,pointer) in selected.items():
        x=conv['entries'][index];assert (x['cohort'],x['pointer'])==(cohort,pointer)
        assert x['controllingDecisions']==['FS-01','FS-02']
        old=x['replacement'];new=old+' '+suffix
        assert at(cohorts[cohort],pointer)==old
        x['controllingDecisions'].append('FEAT327-ACQ-01');x['replacement']=new
        put(cohorts[cohort],pointer,new)
        operations.append({'file':f'{I.relative_to(G).as_posix()}/convention_dispositions.json','pointer':f'/entries/{index}',
                           'entryIdentity':{'cohort':cohort,'pointer':pointer},'oldReplacement':old,'newReplacement':new,
                           'appendedControllingDecision':'FEAT327-ACQ-01','authority':'ACQ-01.2'})
    write(I/'convention_dispositions.json',conv)
    for c,d in cohorts.items():write(I/f'cohorts/{c}.json',d)
    contracts=read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')
    contracts['status']='All335 prerequisite contracts normalized; FEAT327-ACQ-01 bridge fulfilled locally. Full source-qualified actor boundary testing remains pending.'
    contracts.pop('pendingExactIssue');contracts['controllingAddenda']=[info(A/'FEAT327_ACQ_01_GPT_RESPONSE.json')]
    for x in contracts['records']:
        if 'pendingExactIssue' in x:
            x.pop('pendingExactIssue');x['controllingAcquisitionAddendum']='FEAT327-ACQ-01'
        def amend(t):
            if 'bridgeIssue' in t:t['controllingAddendum']=t.pop('bridgeIssue')
            for child in t.get('requirements',[]):amend(child)
        amend(x['requirements'])
        if x['id']=='dragon_blood':
            # Existing full procedure already required this receipt for either printed branch.
            old=deepcopy(x['requirements'])
            x['requirements']={'kind':'all','requirements':[old,{'kind':'actualEstablishedReceipt',
              'receipt':'one recorded actual draconic ancestry damage type for the qualifying lineage source','doesNotCreateSource':True}]}
            x['normalizationCorrection']='Carry the existing final Dragon Blood procedure’s recorded damage-type requirement on both branches. No source rule changed.'
            operations.append({'file':str((A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json').relative_to(G)).replace('\\','/'),
              'id':'dragon_blood','oldRequirements':old,'newRequirements':x['requirements'],'authority':'Existing final dragon_blood completeAuthoringProcedure; local normalization completion, separate from ACQ-01.'})
    contracts['sourceBindings']=[info(G/b['path']) for b in contracts['sourceBindings']]
    contracts['counts']['recordsTouchingPendingWeaponBridge']=0
    contracts['counts']['recordsBoundToCompletedWeaponBridge']=17
    write(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',contracts)
    lines=['# Feat prerequisite contracts','',contracts['scope'],'',contracts['status'],'',
       'This table does not grant feats or prove an actual character history. The exact GPT addendum FEAT327-ACQ-01 now controls the weapon prerequisite bridge. Each full operative feat procedure continues to control its use.','',
       '[Controlling GPT addendum](FEAT327_ACQ_01_GPT_ADDENDUM.md).','',
       '| Original identity | Exact printed prerequisite | Normalized requirement |','|---|---|---|']
    for x in contracts['records']:
        lines.append(f"| `{x['id']}` | {x['printedPrerequisite']} | `{json.dumps(x['requirements'],ensure_ascii=False,separators=(',',':'))}` |")
    lines+=['','The JSON companion preserves each whole original object, full operative procedure, source decision, twelve class counterpart cards and eight unchanged reviewed envelopes.','',
            '[Full source-bound contracts](FEAT_EXACT_01_ACQUISITION_CONTRACTS.json).','']
    (A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md').write_text('\n'.join(lines),encoding='utf-8')

    # Independent finite input vectors, using actual source weapon classifications/properties.
    weapons={x['name']:x for x in read(R/'data/playtest/equipment_source_catalog.json')['records'] if x['name'] in ['Dagger','Shortbow','Greatsword','Longsword','Whip','Longbow']}
    assert len(weapons)==6
    def qualifies(category,proficient):
        for name in proficient:
            w=weapons[name];c=w['category'].lower();properties=w['sourceFields']['Properties'].lower()
            if category=='melee' and 'melee weapons' in c:return True
            if category=='ranged' and 'ranged weapons' in c:return True
            if category=='martial' and c.startswith('martial'):return True
            if category=='Two-Handed' and 'two-handed' in properties:return True
            if category==name:return True
        return False
    checks=[]
    def check(case,name,actual,expected,kind='bounded-reference'):
        checks.append({'case':case,'name':name,'actual':actual,'expected':expected,'pass':actual==expected,'kind':kind})
    for sid in ['bleeding_edge','crippling_strike','disarming_blow','savage_momentum','tactical_flanker']:
        check('ACQ-T01',sid+' actual longsword proficiency, no held item required',qualifies('melee',['Longsword']),True)
    for sid in ['double_tap','target_mark','sure_shot']:check('ACQ-T02',sid+' shortbow profile',qualifies('ranged',['Shortbow']),True)
    check('ACQ-T03','Held but unproficient greatsword supplies no credential',qualifies('Two-Handed',[]),False)
    check('ACQ-T03','Unproficient named whip cannot satisfy named gate',qualifies('Whip',[]),False)
    check('ACQ-T04','Versatile-only longsword fails Two-Handed gate',qualifies('Two-Handed',['Longsword']),False)
    snapshot={'qualifyingProfile':'Greatsword','proficientAtAcquisition':True}
    check('ACQ-T05','Actual proficient Two-Handed acquisition',qualifies('Two-Handed',[snapshot['qualifyingProfile']]),True)
    check('ACQ-T05','Later longsword actually has Versatile/melee profile',('melee weapons' in weapons['Longsword']['category'].lower() and 'Versatile' in weapons['Longsword']['sourceFields']['Properties']),True)
    check('ACQ-T05','Later use does not rewrite acquisition snapshot',snapshot,{'qualifyingProfile':'Greatsword','proficientAtAcquisition':True})
    check('ACQ-T06','Thrown dagger remains melee class',qualifies('ranged',['Dagger']),False)
    check('ACQ-T06','Ranged spell attack with no weapon proficiency',qualifies('ranged',[]),False)
    check('ACQ-T06','Actual longbow is ranged',qualifies('ranged',['Longbow']),True)
    check('ACQ-T07','Unrelated melee proficiency is not Whip',qualifies('Whip',['Longsword']),False)
    check('ACQ-T07','Actual Whip profile qualifies',qualifies('Whip',['Whip']),True)
    check('ACQ-T07','One actual martial profile is sufficient',qualifies('martial',['Longsword']),True)
    check('ACQ-T07','Simple melee is not martial',qualifies('martial',['Dagger']),False)
    check('ACQ-T07','Martial credential alone does not satisfy casting gate',qualifies('martial',['Longsword']) and False,False)
    for gate in ['ability','level','prerequisiteFeat','classAccess','earnedOpportunity']:
        other={x:True for x in ['ability','level','prerequisiteFeat','classAccess','earnedOpportunity']};other[gate]=False
        check('ACQ-T08','Missing '+gate+' rejects despite weapon credential',qualifies('melee',['Longsword']) and all(other.values()),False)
    # These final use-time sentences are source adjudications, not full attack simulations.
    pub={x['id']:x for x in read(U/'candidate.json')['feats']}
    check('ACQ-T09','Target Mark retains actual melee reach permission','current melee reach or printed maximum ranged range' in pub['target_mark']['operationalRules'],True,'source-adjudication')
    check('ACQ-T09','Weapon Focus retains actual ongoing proficiency','while that proficiency remains operative' in pub['weaponFocus']['operationalRules'],True,'source-adjudication')
    check('ACQ-T09','Weapon Mastery remains nonrepeatable','permanent choice, nonrepeatable' in pub['weapon_mastery']['operationalRules'],True,'source-adjudication')
    check('ACQ-T05','Cleaving Momentum retains permitted Versatile use','a legal Versatile two-hand attack can operate the acquired feat' in pub['cleaving_momentum']['operationalRules'],True,'source-adjudication')

    # Verify exactly the approved shared-rule change; untouched source books/catalogs retain bindings.
    build=read(A/'FEAT_EXACT_CANDIDATE_01_BUILD.json');descendants={p.relative_to(G).as_posix():info(p) for p in outputs}
    for rel,b in build['originalSourceBindings'].items():
        check('PRESERVE','Original input '+rel,{k:info(G/rel)[k] for k in ['bytes','sha256']},b,'input-integrity')
    for rel,b in build['artifacts'].items():
        if rel not in descendants:check('PRESERVE','Unchanged candidate artifact '+rel,{k:info(G/rel)[k] for k in ['bytes','sha256']},b,'input-integrity')
    original_shared=read(G/snapshot[(I/'shared_rules.json').relative_to(G).as_posix()]['preservedCopy'])
    desired=deepcopy(original_shared);desired['rules'][1]['wording']=desired['rules'][1]['wording'].replace(anchor,anchor+'\n\n'+paragraph)
    check('ACQ-01.1','Complete internal shared contract equals exact insertion',read(I/'shared_rules.json')==desired,True,'complete-structure')
    check('ACQ-01.1','Complete public contract equals internal',read(U/'shared_rules.json')==desired,True,'complete-structure')
    old_conv=read(G/snapshot[(I/'convention_dispositions.json').relative_to(G).as_posix()]['preservedCopy'])
    expected=deepcopy(old_conv)
    for i in selected:expected['entries'][i]['controllingDecisions'].append('FEAT327-ACQ-01');expected['entries'][i]['replacement']+=' '+suffix
    check('ACQ-01.2','All91 entries equal exactly four authorized amendments',conv==expected,True,'complete-structure')
    check('ACQ-01.1','Reader contains exact full paragraph',(D/'SHARED_RULES.md').read_text('utf-8').count(paragraph),1,'complete-text')
    failures=[x for x in checks if not x['pass']]
    expected_cases=[]
    for line in answer.splitlines():
        mt=re.match(r'\| \*\*(ACQ-T\d+) — (.*?)\*\* \| (.*?) \|$',line)
        if mt:expected_cases.append({'id':mt[1],'name':mt[2],'completeExpectedOutcome':mt[3]})
    assert len(expected_cases)==9 and {x['id'] for x in expected_cases}<={x['case'] for x in checks}
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'correctionId':'FEAT327-ACQ-01','status':'finite named correction fulfilled locally' if not failures else 'failed local finite checks',
      'sourceReply':info(A/'FEAT327_ACQ_01_GPT_RESPONSE.json'),'sourceAddendum':info(A/'FEAT327_ACQ_01_GPT_ADDENDUM.md'),
      'preservationManifest':info(A/'feat-exact-01-before-acq01/PRESERVATION_MANIFEST.json'),'operations':operations,
      'measuredCurrentDescendants':descendants,'sourceWeaponProfiles':weapons,'sourceWeaponBinding':info(R/'data/playtest/equipment_source_catalog.json'),
      'expectedCases':expected_cases,'checks':len(checks),'failureCount':len(failures),'failures':failures,'results':checks,
      'referenceScope':'Weapon credential predicates and source-based use-time adjudications; actual other prerequisites/opportunities remain separate required facts. No full attack runtime.',
      'separateLocalNormalizationCorrection':'Dragon Blood recorded damage-type requirement applies on either branch under its existing final procedure; no new game rule.',
      'onlyThisNamedIssueClosed':not failures,'candidateExactApproved':False,'candidateReadyForSubmission':False,'sourceInformationDeleted':0,
      'immutableSourceArchive':info(A/'DD_Feats_327_Final_Source_Verdict_and_Evidence.zip'),
      'doNotRerunObsoleteChecks':'Assembly/structure/first-boundary reports bind the pre-ACQ seven derived candidates. They remain historical. This receipt supplies exact current descendant bindings; update future validators with this lineage, never rewrite old hashes.'}
    write(receipt,result)
    print(json.dumps({'receipt':info(receipt),'descendants':len(descendants),'checks':len(checks),'failures':len(failures),'failedNames':[x['name'] for x in failures],'onlyNamedIssueClosed':not failures}))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
