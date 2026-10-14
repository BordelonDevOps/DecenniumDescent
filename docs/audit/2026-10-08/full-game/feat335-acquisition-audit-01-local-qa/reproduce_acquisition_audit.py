#!/usr/bin/env python3
"""Read-only, standard-library source joins and narrow acquisition counterexamples.

No original validator is run, no game runtime is implemented, no campaign premise
is authenticated. Only the explicit output directory receives reports.
"""
from __future__ import annotations
import argparse, ast, copy, hashlib, json, sys, tempfile, types, zipfile
from pathlib import Path
sys.dont_write_bytecode = True
P = 'DescentReviewChanges/ReviewBible/'
A = 'docs/audit/2026-10-08/full-game/'
CP=A+'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
PP=P+'data/public/feat_candidates/exact_01/candidate.json'
IP=P+'data/director/feat_candidates/exact_01/candidate.json'
SUP=P+'data/public/feat_candidates/exact_01/supplements.json'

def audit(root: Path, out: Path):
    checks=[]; observations=[]
    def read(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
    def check(name, passed, kind='source-reference', detail=None):
        row={'id':name,'kind':kind,'passed':bool(passed)}
        if detail is not None:row['detail']=detail
        checks.append(row)
        if not passed:raise AssertionError(name)
    manifest=read('PACKAGE_MANIFEST.json')
    for path, spec in manifest.items():
        raw=(root/path).read_bytes()
        check('manifest/'+path,len(raw)==spec['bytes'] and hashlib.sha256(raw).hexdigest()==spec['sha256'],'payload-integrity')
    contracts=read(CP)['records']; public=read(PP); internal=read(IP)
    cm={r['id']:r for r in contracts}; pm={r['id']:r for r in public['feats']}; im={r['id']:r for r in internal['records']}
    check('335-unique-contracts',len(cm)==len(contracts)==335)
    check('335-public-identities',len(pm)==335 and set(pm)==set(cm))
    check('327-current-internal-plus-eight-retained',len(im)==327 and len(internal['unchangedReviewedFeats'])==8)
    check('immutable-registry-335',len(internal['original335Registry'])==335)
    nulls=[]
    for i,r in enumerate(contracts):
        sid=r['id']; p=pm[sid]
        check('source-object/'+sid,r['originalObject']==p['sourceObject'],'complete-object-equality')
        if sid in im:
            q=im[sid]
            check('internal-source/'+sid,q['sourceObject']==r['originalObject'],'complete-object-equality')
            check('current-procedure-parity/'+sid,p['operationalRules']==q['operationalRules']==r['completeOperativeProcedure'],'complete-procedure-equality')
            check('payload-parity/'+sid,p['payloadOperational']==q['payloadOperational'],'complete-payload-equality')
            if p['payloadOperational'] is None:nulls.append(sid)
        else:
            check('eight-own-complete-procedures/'+sid,len(r['completeOperativeProcedure'])>100 and 'unchangedReviewedRecord' in p,'retained-scope')
    check('two-null-outlines',set(nulls)=={'astral_projection','planar_binding'},'retained-scope')
    groups=read(SUP)['groups']; supp={g['id']:g['value'] for g in groups}
    catalog={r['id']:r for r in read(P+'data/public/spell_playtests/catalog.json')['spells']}
    placements=0
    for curriculum,v in supp['SUP-04'].items():
        rows=v['choices']; placements+=len(rows)
        check('curriculum-count/'+curriculum,sum(r['rank']==0 for r in rows)==v['rank0Choices'] and sum(r['rank']==1 for r in rows)==v['rank1Choices'])
        for i,r in enumerate(rows):
            access=catalog[r['id']]['classAccess'][r['sourceClass']]
            check('curriculum-placement/'+curriculum+'/'+str(i),access==r['fullOriginalClassAccessRow'] and access['rank']==r['rank'] and access['school']==r['school'],'exact-menu-source-join')
    check('sixteen-curricula',len(supp['SUP-04'])==16)
    check('physical-casting-curricula',supp['SUP-04']['Dragoon']['featCastingAbility']=='STR' and supp['SUP-04']['Monk']['featCastingAbility']=='DEX' and supp['SUP-04']['Thief']['featCastingAbility']=='DEX')
    check('flora-provider-source', 'At acquisition select one actual possessed spellcasting route' in supp['SUP-07']['floraBody']['dc'])

    # Full dependency envelopes are equality-checked, not promoted as new spells.
    deps_all=read(P+'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells']
    cache={}
    def pointer(obj,path):
        for token in path.strip('/').split('/') if path else []:
            token=token.replace('~1','/').replace('~0','~')
            obj=obj[int(token)] if isinstance(obj,list) else obj[token]
        return obj
    for sid,dep in deps_all.items():
        b=dep['binding']; path=b['file']
        if path not in cache:cache[path]=read(path)
        check('dependency-whole-card/'+sid,pointer(cache[path],b['pointer'])==dep['completeCurrentProcedureCard'],'complete-dependency-equality')
        check('dependency-original/'+sid,dep['originalCatalogRecord']==catalog[sid],'complete-dependency-equality')
    # Source-defined report-capture functions, isolated from validator main().
    snapshot_inventory=[]
    report_names=['FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json','FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json']
    for report_name in report_names:
        report=read(A+report_name)
        for i,r in enumerate(report['results']):
            if isinstance(r,dict) and 'actual' in r and 'expected' in r and r.get('pass',r.get('passed')) is True and r['actual']!=r['expected']:
                snapshot_inventory.append({'path':A+report_name,'pointer':'/results/'+str(i),'capturedRow':copy.deepcopy(r)})
    check('snapshot-defect-count',len(snapshot_inventory)==559,'expected-baseline-defect')
    for stem in ['acquisition_history','numeric_prerequisites']:
        path=P+'tools/validate_feat_exact_01_'+stem+'.py'
        tree=ast.parse((root/path).read_text(encoding='utf-8'))
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='normalized']
        main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        ck=next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='check')
        ns={'checks':[],'deepcopy':copy.deepcopy}
        exec(compile(ast.Module(body=nodes+[ck],type_ignores=[]),path,'exec'),ns)
        actual={'opportunity':{'spent':False}}; expected=copy.deepcopy(actual)
        if stem=='acquisition_history':ns['check']('before-later-payment',actual,expected)
        else:ns['check']('before-later-payment','opportunity-history',actual,expected)
        actual['opportunity']['spent']=True
        row=ns['checks'][0]
        check('mutable-capture-reproduced/'+stem,row['actual']!=row['expected'] and row.get('pass',row.get('passed')) is True,'expected-baseline-defect')
        a={'opportunity':{'spent':False}}; e=copy.deepcopy(a)
        held={'actual':copy.deepcopy(a),'expected':copy.deepcopy(e)};held['passed']=held['actual']==held['expected']
        a['opportunity']['spent']=True
        check('immutable-capture-reference/'+stem,held['actual']==held['expected'] and held['passed'],'focused-corrected-reference')
    out.mkdir(parents=True,exist_ok=True)
    (out/'REPORT_SNAPSHOT_MISMATCHES.json').write_text(json.dumps({'status':'Observed historical evidence serialization defects; not 559 inferred rule failures','count':len(snapshot_inventory),'rows':snapshot_inventory},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    # Only import bounded local models. No submitted validator main() executes.
    sys.path.insert(0,str(root/P/'tools'))
    from feat_exact_01_casting_credential_model import CastingSources
    from feat_exact_01_remaining_owned_chains import RemainingOwnedChains
    from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
    foundation=read(P+'data/playtest/character_foundation.json')
    classes={r['class']:r for r in foundation['classes']}
    skills={s:a for a,ss in foundation['skillAbilities'].items() for s in ss}
    ancestry=read(P+'data/playtest/ancestry_background_candidate.json')
    backgrounds={r['id']:r for r in ancestry['backgrounds']}
    equip={r['id']:r for r in read(P+'data/playtest/equipment_source_catalog.json')['records']}
    deps=read(P+'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells']
    wizard=read(P+'data/public/class_playtests/wizard.json')
    initiate_report=read(A+'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json')
    base=copy.deepcopy(initiate_report['actorSourceProjection'])
    base['selectedClassSkills']=['Nature','Athletics']
    sources=CastingSources(root,deps,supp,wizard)
    choices=initiate_report['authoredCurriculumChoices']
    if isinstance(choices,list):choices={r['curriculum']:r for r in choices}
    # Submitted helper patched in memory only. The serialized diff is separate.
    model_path=P+'tools/feat_exact_01_remaining_owned_chains.py'
    old=(root/model_path).read_text(encoding='utf-8')
    needle="        elif choice is not None:\n            raise ValueError('No permanent acquisition menu exists for this named procedure')"
    patch="        elif sid == 'conjure_flora':\n            if choice not in self.actual_casting_routes():\n                raise ValueError('Permanently select an actual owned casting route')\n            additions = {'fixedCastingRoute': deepcopy(choice)}\n"+needle
    block="""        elif sid == 'conjure_flora':
            additions = {'creationUses': {'maximum': 1, 'current': 1},
                         'plantCapacity': 2 if level >= 10 else 1, 'activePlants': [],
                         'additionalCreationPending': False}"""
    block2="""        elif sid == 'conjure_flora':
            additions.update({'creationUses': {'maximum': 1, 'current': 1},
                              'plantCapacity': 2 if level >= 10 else 1, 'activePlants': [],
                              'additionalCreationPending': False})"""
    ability="if ability not in {'INT', 'WIS', 'CHA'}:"
    for label,text in [('selection',needle),('flora-init',block),('ability-filter',ability)]:
        check('guard/'+label,old.count(text)==1,'guarded-reference-edit')
    fixed=old.replace(ability,"if ability not in {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'}:").replace(needle,patch).replace(block,block2)
    module=types.ModuleType('reviewer_patched_remaining_chains')
    exec(compile(fixed,'<in-memory scoped corrected reference>','exec'),module.__dict__)
    Fixed=module.RemainingOwnedChains
    def history(cls,curriculum):
        actor=copy.deepcopy(base)
        h=cls(actor,classes,equip,skills,ancestry,backgrounds,cm,supp,sources)
        paid=InitiateAcquisitions(actor,classes,equip,skills,ancestry,backgrounds,cm,supp['SUP-04'],deps)
        paid.advance(4);paid.earn(4)
        choice=choices[curriculum]
        if isinstance(choice,list):choice={'curriculum':curriculum,'cantrips':choice[1],'rank1':choice[2]}
        if 'selectedChoice' in choice:choice=choice['selectedChoice']
        paid.acquire('magicInitiate',4,choice)
        h.advance(4);h.pay=paid.pay;h.casting.import_initiate(paid,4)
        h.advance(8);h.earn(8)
        return h
    def reject(label,h,call):
        before=h.snapshot()
        try:call()
        except (ValueError,KeyError) as exc:
            check(label,True,'focused-rejection',str(exc))
        else:check(label,False,'focused-rejection')
        check(label+'/atomic',before==h.snapshot(),'focused-state-integrity')
    oldh=history(RemainingOwnedChains,'Wizard')
    oldh.acquire_named('conjure_flora',8)
    obs={'id':'BASELINE-FLORA-MISSING-PROVIDER','classification':'REPRODUCED_SOURCE_MISMATCH',
         'acceptedWithoutProvider': 'fixedCastingRoute' not in oldh.initializations['conjure_flora'],
         'actualInitialState':copy.deepcopy(oldh.initializations['conjure_flora'])}
    observations.append(obs)
    check('baseline-reproduces-missing-flora-provider',obs['acceptedWithoutProvider'],'expected-baseline-defect')
    f=history(Fixed,'Wizard')
    reject('fixed-flora-rejects-no-provider',f,lambda:f.acquire_named('conjure_flora',8))
    reject('fixed-flora-rejects-foreign-provider',f,lambda:f.acquire_named('conjure_flora',8,{'grantId':'not-owned','ability':'INT','sourceClass':'Wizard'}))
    route=f.actual_casting_routes()[0];f.acquire_named('conjure_flora',8,route)
    check('fixed-flora-records-provider',f.initializations['conjure_flora']['fixedCastingRoute']==route,'focused-corrected-reference')
    check('fixed-flora-no-body-no-additional-creation',f.initializations['conjure_flora']['activePlants']==[] and not f.initializations['conjure_flora']['additionalCreationPending'],'focused-corrected-reference')
    f.initializations['conjure_flora']['creationUses']['current']=0;f.advance(12)
    check('flora-growth-no-refill',f.initializations['conjure_flora']['plantCapacity']==2 and f.initializations['conjure_flora']['creationUses']['current']==0,'focused-corrected-reference')
    for curriculum in ['Dragoon','Monk','Thief']:
        h=history(RemainingOwnedChains,curriculum)
        try:h.actual_casting_routes()
        except ValueError as exc:observations.append({'id':'BASELINE-PROVIDER-'+curriculum,'classification':'REPRODUCED_SOURCE_MISMATCH','error':str(exc)});check('baseline-rejects-legal-'+curriculum,True,'expected-baseline-defect')
        else:check('baseline-rejects-legal-'+curriculum,False,'expected-baseline-defect')
        h=history(Fixed,curriculum); routes=h.actual_casting_routes()
        check('fixed-provider/'+curriculum,bool(routes) and {r['ability'] for r in routes}=={supp['SUP-04'][curriculum]['featCastingAbility']},'focused-corrected-reference')
        h.acquire_named('conjure_flora',8,routes[0])
        check('fixed-flora-physical-ability/'+curriculum,h.initializations['conjure_flora']['fixedCastingRoute']==routes[0],'focused-corrected-reference')
        h=history(Fixed,curriculum);h.acquire_named('stormcaller',8,h.actual_casting_routes()[0]);h.advance(12);h.earn(12)
        chosen={'ability':supp['SUP-04'][curriculum]['featCastingAbility']}
        reject('no-INT-fallback-with-real-route/'+curriculum,h,lambda:h.acquire_named('voltyros_pact',12,{'ability':'INT'}))
        h.acquire_named('voltyros_pact',12,chosen)
        check('voltyros-keeps-real-source/'+curriculum,h.initializations['voltyros_pact']['fixedAbility']==chosen['ability'] and not h.initializations['voltyros_pact']['noCastingFallback'],'focused-corrected-reference')
    # Classification sources, not an executed CRPG proficiency adapter.
    unarmed=next(r for r in equip.values() if r['id']=='simple-melee-weapons.unarmed-strike')
    check('unarmed-source-simple-melee',unarmed['category']=='Simple melee weapons')
    check('monk-simple-training-source','Simple weapons' in classes['Monk']['weapons'])
    claws=next(t for a in ancestry['ancestries'] if a['id']=='troll' for t in a['traits'] if t['id']=='troll--claws')
    text=json.dumps(claws,ensure_ascii=False)
    check('troll-explicit-unarmed-source','natural weapons' in text and 'unarmed strikes' in text)
    check('tavern-actual-unarmed-proficiency','Gain actual improvised-weapon and unarmed-strike proficiency.' in cm['tavern_brawler']['completeOperativeProcedure'])
    check('focus-ongoing-proficiency','while that proficiency remains operative' in cm['weaponFocus']['completeOperativeProcedure'])
    check('mastery-acquisition-proficiency','At acquisition, choose one actual weapon profile/type in which you are proficient' in cm['weapon_mastery']['completeOperativeProcedure'])
    # Finite adjudication references: raw 19 must hit; raw20 auto-hits; no runtime claim.
    for raw,total,ac,want in [(19,19,20,False),(19,20,20,True),(20,9,30,True)]:
        got=raw==20 or (raw==19 and total>=ac)
        check(f'critical-boundary/{raw}/{total}/{ac}',got==want,'independent-reference-arithmetic')
    check('broadest-not-additive',min(20,19,18)==18,'independent-reference-arithmetic')
    # Final rehash catches accidental imports/report-writes affecting any input.
    for path,spec in manifest.items():
        check('unchanged-after/'+path,hashlib.sha256((root/path).read_bytes()).hexdigest()==spec['sha256'],'post-inspection-preservation')
    report={'auditId':'FEAT335-ACQUISITION-AUDIT-01','executedByThisReview':True,
       'scope':'Read-only full-source joins, guarded in-memory two-model corrections, paid source-qualified synthetic counterexamples and four independent arithmetic boundaries. Not any submitted suite rerun or full acquisition/runtime engine.',
       'manifestSha256':hashlib.sha256((root/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest(),
       'counts':{'payloads':len(manifest),'contracts':len(cm),'curricula':16,'sourcePlacementRows':placements,'fullDependencyEnvelopes':len(deps_all),'reportedSnapshotMismatches':len(snapshot_inventory),
                 'checks':len(checks),'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)},
       'baselineDefects':observations,'checks':checks,'originalValidatorsRerun':False,
       'originalInputsChanged':False,'campaignAuthenticated':False,'runtimeCertified':False,'candidateApproved':False}
    out.mkdir(parents=True,exist_ok=True)
    (out/'REPRODUCTION_RESULTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report['counts']))

if __name__=='__main__':
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--submission',type=Path);g.add_argument('--archive',type=Path)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    if args.submission:audit(args.submission,args.output)
    else:
        with tempfile.TemporaryDirectory(prefix='feat335_readonly_') as d:
            root=Path(d)
            with zipfile.ZipFile(args.archive) as z:
                for item in z.infolist():
                    target=(root/item.filename).resolve()
                    if root.resolve() not in target.parents:raise ValueError('Unsafe ZIP member')
                z.extractall(root)
            audit(root,args.output)
