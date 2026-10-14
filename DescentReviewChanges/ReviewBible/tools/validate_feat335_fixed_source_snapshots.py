"""FW07/AA16 source descriptors joined to actual paid fixed snapshot histories."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from pathlib import Path
from feat335_fixed_source_snapshots import TrainingSnapshots,LineageSnapshots,BRANCHING,FIXED,TOOLS
from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_acquisition_models import FixedTraining
from validate_feat_exact_01_composite_casting import read,info,serial

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'


def main():
    out=A/'FEAT335_FIXED_SOURCE_SNAPSHOT_CHECK.json';desc=A/'FEAT335_FIXED_SOURCE_SNAPSHOT_DESCRIPTORS.json'
    assert not out.exists() and not desc.exists()
    paths=[R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json',R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R/'data/public/feat_candidates/exact_01/candidate.json',R/'data/public/class_playtests/monk.json',
        R/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md',
        A/'feat335-acquisition-audit-01-verdict/ACQUISITION_ROWS.json',
        A/'feat335-acquisition-audit-01-verdict/FINITE_REMAINING_WORK.json',
        A/'FEAT335_FAA03_UNARMED_PROFILE_CHECK.json',
        A/'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_FAA04_CHECK.json',
        A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json',Path(__file__),
        *[R/'tools'/n for n in ['feat335_fixed_source_snapshots.py','feat335_source_unarmed_choices.py',
            'feat_exact_01_acquisition_models.py','feat_exact_01_lineage_prerequisite_model.py',
            'feat_exact_01_training_prerequisite_model.py','feat_exact_01_prodigy_choices.py',
            'feat_exact_01_composite_casting_model.py','feat_exact_01_casting_credential_model.py',
            'maximum_hp_playtest_rules.py','core_playtest_rules.py','strain_playtest_rules.py',
            'spell_playtest_rules.py','control_playtest_rules.py']]]
    bindings=[info(p) for p in paths]
    f,ancestry,eq,sp,deps,wizard,cd,prior=[read(p) for p in paths[:8]]
    classes={x['class']:x for x in f['classes']};skills={s:a for a,group in f['skillAbilities'].items() for s in group}
    equipment={x['id']:x for x in eq['records']};backgrounds={x['id']:x for x in ancestry['backgrounds']}
    contracts={x['id']:x for x in cd['records']};supp={x['id']:x['value'] for x in sp['groups']}
    sources=CastingSources(G,deps['spells'],supp,wizard);public={x['id']:x for x in read(paths[8])['feats']}
    monk=read(paths[9]);trade=paths[10].read_text(encoding='utf-8')
    rows={x['id']:x for x in read(paths[11])['rows']};group=next(g for g in read(paths[12])['groups'] if g['id']=='FW-07')
    checks=[];histories=[];descriptor_rows=[]

    def check(label,truth,details=None):
        checks.append({'id':label,'passed':bool(truth),'details':deepcopy(details)})
        assert truth,label

    def reject(label,h,action):
        before=h.snapshot()
        try:action()
        except ValueError as error:check(label+'/rejected',True,str(error))
        else:check(label+'/rejected',False)
        check(label+'/atomic',h.snapshot()==before)

    def op(h,level):h.advance(level);h.earn(level)

    def training(sid,trained):
        first='Shaman' if sid=='herbalist' and trained else 'Thief' if sid=='burglar' and trained else 'Bard' if trained else 'Warrior'
        actor=deepcopy(prior['actorSourceProjection']);actor.update(firstClass=first,classLevels={first:1})
        existing={'Reputation','Persuasion','History','Performance'}
        targets=BRANCHING.get(sid,FIXED.get(sid,['Nature'] if sid=='herbalist' else []))
        selected=[s for s in targets if s not in existing and s in classes[first]['skillOptions']] if trained or sid=='herbalist' else []
        eligible=[s for s in classes[first]['skillOptions'] if s not in existing and s not in selected]
        # Prefer other skills for the untrained witness when the actual class allows it.
        eligible=sorted(eligible,key=lambda s:(s in targets,s))
        selected=(selected+eligible)[:classes[first]['skillChoices']]
        actor['selectedClassSkills']=selected
        actor['classToolChoices']=[sid for sid,row in equipment.items() if row.get('group')=='Musical Instruments'][:3] if first=='Bard' else []
        return TrainingSnapshots(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supp,sources,trade_reference=trade)

    def lineage(aid='human',vid='imperial-human'):
        base=next(x for x in ancestry['ancestries'] if x['id']==aid);variant=next(x for x in base['variants'] if x['id']==vid)
        rolls={a:[1,3,6,6] for a in ['STR','DEX','CON','INT','WIS','CHA']}
        actor={'firstClass':'Warrior','classLevels':{'Warrior':1},'priorFeatChoices':[],
            'ancestryId':aid,'variantId':vid,'abilityRolls':rolls,
            'permanentScores':{a:15+variant['combinedAbilityBonuses'].get(a,0) for a in rolls},'physicalInventory':[]}
        return LineageSnapshots(actor,ancestry,classes,equipment,contracts,monk['engine'][17])

    for sid in group['exactMembers']:
        operative=public[sid].get('unchangedReviewedRecord',public[sid])['operationalRules']
        check(sid+'/complete-current-GPT-procedure-join',contracts[sid]['completeOperativeProcedure']==operative==rows[sid]['a_acquisition']['completeControllingOperativeProcedure'])
    check('exact21-identity-join',set(group['exactMembers'])==set(BRANCHING)|set(FIXED)|set(TOOLS)|{'tavern_brawler','tough','tenacity','tough_as_nails','night_hunter','dark_affinity','cultural_legacy'})

    for sid in sorted(set(BRANCHING)|set(FIXED)|set(TOOLS)):
        for trained in [False,True]:
            h=training(sid,trained);op(h,8);before=h.snapshot();tag=sid+'/'+str(trained)
            if sid=='herbalist' and trained:
                # Actual class supplies the kit proficiency; the advanced progression is conditional prior state.
                trade_name=h.primary[TOOLS[sid]];h.trades[trade_name]={'level':4,'xp':90}
            prior_trades=deepcopy(h.trades);prior_skills=deepcopy(h.training_projection['skills']);prior_tools=set(h.training_projection['tools'])
            event=h.acquire_fixed_training(sid,8)
            check(tag+'/paid-and-no-extra-permanent-menu',event['grant']['opportunity']==h.first+':8' and event['grant']['choice'] is None)
            check(tag+'/no-inventory-or-class-change',h.actor['physicalInventory']==[] and h.pay.current_classes=={h.first:8})
            check(tag+'/no-extra-grants',event['physicalItemsGranted']==event['newCoursesOrFacts']==[])
            if sid in BRANCHING or sid in FIXED:
                recipients=BRANCHING.get(sid,FIXED.get(sid))
                expected={s:(2 if sid in BRANCHING and prior_skills.get(s,0)>=1 else 1) for s in recipients}
                check(tag+'/exact-fixed-recipient-branches',event['fixedBranches']==expected,event['fixedBranches'])
                check(tag+'/no-recipient-spill',all(h.training_projection['skills'].get(s,0)==prior_skills.get(s,0) for s in skills if s not in recipients))
                check(tag+'/no-tool-or-trade-grant',h.training_projection['tools']==prior_tools and h.trades==prior_trades)
                fixed=deepcopy(h.fixed_training.branches[sid])
                for skill in recipients:
                    for independent in [1,2]:
                        check(tag+'/'+skill+'/later-independent/'+str(independent),h.fixed_training.contribution(sid,skill,independent)==max(fixed[skill],independent))
                    h.fixed_training.suppressed.add(sid)
                    check(tag+'/'+skill+'/suppressed-keeps-independent',h.fixed_training.contribution(sid,skill,1)==1)
                    h.fixed_training.suppressed.clear()
                h.advance(12)
                check(tag+'/advancement-does-not-reselect',h.fixed_training.branches[sid]==fixed)
            else:
                check(tag+'/exact-fixed-tool-only',h.training_projection['tools']==prior_tools|{TOOLS[sid]} and h.training_projection['skills']==prior_skills)
                if sid=='burglar':check(tag+'/no-trade-level-from-Burglar',h.trades==prior_trades)
                else:
                    tn=h.primary[TOOLS[sid]]
                    check(tag+'/mapped-Herbalism-only',tn=='Herbalism' and h.trades[tn]==prior_trades.get(tn,{'level':1,'xp':0}) and
                          {k:v for k,v in h.trades.items() if k!=tn}=={k:v for k,v in prior_trades.items() if k!=tn})
                h.advance(12)
            h.earn(12);reject(tag+'/duplicate-no-reselection',h,lambda:h.acquire_fixed_training(sid,12))
            histories.append({'id':tag,'feat':sid,'before':before,'paidAcquisition':event,'after':h.snapshot(),
                'conditionalBoundaries':'Independent later factor/suppression probes; Herbalism4/90 fixture, if present, is not newly earned XP.'})

    # Reuse the shared branch algebra for two additional explicitly source-matched entries.
    for sid in ['acrobat','animalAffinity']:
        skill=BRANCHING[sid][0]
        for prior_factor in [0,1,2]:
            model=FixedTraining();branch=model.acquire(sid,{skill:'snapshot-proficiency-or-expertise'},{skill:prior_factor})
            check(sid+'/shared-factor-boundary/'+str(prior_factor),branch[skill]==(1 if prior_factor==0 else 2))
            check(sid+'/no-four-PB/'+str(prior_factor),model.contribution(sid,skill,2)==2)

    for sid in ['night_hunter','dark_affinity']:
        for aid,vid,base_range in [('human','imperial-human',0),('troll','swamp-troll',60),('umbrin','obsidian-highborn',120)]:
            h=lineage(aid,vid);op(h,8);before=h.snapshot();h.acquire_snapshot(sid,8);tag=sid+'/'+aid
            check(tag+'/actual-source-range',max([0]+[x['range'] for x in h.independent_vision])==base_range)
            check(tag+'/fixed-mode-and-current-range',h.vision[sid].branch==('extension30' if base_range else 'base60') and h.vision_range(sid)==(base_range+30 if base_range else 60))
            fixed=deepcopy(h.initializations[sid]);h.vision[sid].operative=False
            check(tag+'/suppression-leaves-independent-source',h.vision_range(sid)==base_range)
            h.vision[sid].operative=True
            check(tag+'/no-underlying-source-no-extension-fallback',h.vision_range(sid,[])==(0 if base_range else 60))
            check(tag+'/later-stronger-source-no-reselection',h.vision_range(sid,[120])==(150 if base_range else 120) and h.initializations[sid]==fixed)
            op(h,12);reject(tag+'/no-new-purchase',h,lambda:h.acquire_snapshot(sid,12))
            histories.append({'id':tag,'feat':sid,'before':before,'after':h.snapshot(),'conditionalBoundaries':'Later independent source loss/addition and suppression are queries, not ancestry conversions.'})

    h=lineage();op(h,4);before=h.snapshot();h.acquire_snapshot('tough',4)
    check('HP/Tough-fixed-at-four',h.hp_events[-1]['additiveBonuses']==8 and h.life.hp==7)
    op(h,8);h.acquire_snapshot('tenacity',8)
    check('HP/Tough-plus-live-Tenacity-at-eight',h.hp_events[-1]['additiveBonuses']==16 and h.life.hp==7)
    op(h,12);h.acquire_snapshot('tough_as_nails',12);h.advance(14)
    check('HP/three-distinct-source-amounts',h.hp_events[-1]['additiveBonuses']==8+14+28 and h.life.hp==7)
    contributions=deepcopy(h.hp_sources['tough_as_nails']['levelContributions'])
    h.conditional_level_loss_or_restoration(13)
    check('HP/conditional-loss-removes-one-nails-contribution',h.hp_events[-1]['additiveBonuses']==8+13+26)
    h.conditional_level_loss_or_restoration(14);h.conditional_level_loss_or_restoration(14)
    check('HP/same-level-restoration-once',h.hp_events[-1]['additiveBonuses']==8+14+28 and h.hp_sources['tough_as_nails']['levelContributions']==contributions)
    h.life.hp=h.life.maximum_hp # Explicit conditional prior healing to test a capacity clamp, not performed by this feat.
    h.pay.suppress('tough');event=h.recompute_hp()
    check('HP/suppression-clamps-without-damage-healing',event['capacityClamp']==8 and event['actualHpDamage']==event['actualHpGained']==event['woundSaves']==event['deathFailuresAdded']==0)
    clamped=h.life.hp;h.pay.suppress('tough',False);h.recompute_hp()
    check('HP/restoration-capacity-only-fixed-snapshot',h.life.hp==clamped and h.hp_sources['tough']['acquisitionLevel']==4)
    op(h,16)
    for sid in ['tough','tenacity','tough_as_nails']:reject('HP/'+sid+'/nonrepeatable',h,lambda sid=sid:h.acquire_snapshot(sid,16))
    histories.append({'id':'three-paid-distinct-HP-identities','feats':['tough','tenacity','tough_as_nails'],'before':before,'after':h.snapshot(),
        'conditionalBoundaries':'Separately authorized level loss/restoration and prior healing are conditional inputs. No retraining, loss or healing mechanic granted.'})
    h=lineage();op(h,4);reject('HP/Nails-level-four-gate',h,lambda:h.acquire_snapshot('tough_as_nails',4))
    h=lineage();h.advance(12);h.earn(4);h.acquire_snapshot('tough',4)
    check('HP/Tough-snapshots-actual-attained-not-old-opportunity',h.hp_sources['tough']['acquisitionLevel']==12 and h.hp_events[-1]['additiveBonuses']==24)
    histories.append({'id':'Tough-banked-opportunity-current-acquisition','feat':'tough','after':h.snapshot()})

    for variant in ['boom-goblin','scrap-goblin','shadow-goblin']:
        h=lineage('goblin',variant);op(h,4);before=h.snapshot();h.acquire_snapshot('cultural_legacy',4)
        check(variant+'/actual-selected-variant-fixed',h.initializations['cultural_legacy']['fixedVariantId']==variant)
        check(variant+'/no-training-or-item-granted',h.initializations['cultural_legacy']['proficiencyGranted']==h.initializations['cultural_legacy']['physicalItemsGranted']==[])
        for total in [-1,0,9,10,19,20]:
            check(variant+'/Stealth-signed-total/'+str(total),h.cultural_bonus('DEX','Stealth','hiding',total)==max(0,total)//10)
        check(variant+'/Boom-exact-INT-task',h.cultural_bonus('INT',None,'explosives',20)==(2 if variant=='boom-goblin' else 0))
        check(variant+'/not-any-explosive-roll',h.cultural_bonus('DEX',None,'explosives',20)==0)
        check(variant+'/Scrap-exact-recipients',h.cultural_bonus('WIS','Perception','useful-junk',20)==(2 if variant=='scrap-goblin' else 0) and
              h.cultural_bonus('DEX','Sleight of Hand','hidden-objects',20)==(2 if variant=='scrap-goblin' else 0))
        check(variant+'/not-generic-Perception-or-passive',h.cultural_bonus('WIS','Perception','watching-enemy',20)==0 and h.cultural_bonus('DEX','Stealth','hiding',20,rolled=False)==0)
        saved=deepcopy(h.initializations['cultural_legacy']);h.pay.suppress('cultural_legacy')
        check(variant+'/suppressed-no-bonus',h.cultural_bonus('DEX','Stealth','hiding',20)==0)
        h.pay.suppress('cultural_legacy',False);op(h,8)
        reject(variant+'/no-variant-repurchase',h,lambda:h.acquire_snapshot('cultural_legacy',8))
        check(variant+'/retains-original-variant-record',h.initializations['cultural_legacy']==saved)
        histories.append({'id':variant+'/Cultural-Legacy','feat':'cultural_legacy','before':before,'after':h.snapshot()})
    h=lineage();op(h,4);reject('Human-is-not-Goblin-by-feat-name',h,lambda:h.acquire_snapshot('cultural_legacy',4))

    # Reuse the completed paid Tavern Brawler source histories, not a new replacement scenario.
    tavern=read(paths[13]);check('Tavern/existing-source-qualified-report-pass',tavern['failed']==0)
    tavern_pointers=[]
    for i,history in enumerate(tavern['histories']):
        grants=history['after']['payment']['grants']
        if any(x['identity']=='tavern_brawler' for x in grants):
            check('Tavern/'+str(i)+'/actual-paid-training',any(x['identity']=='tavern_brawler' and x['opportunity'].endswith(':4') for x in grants))
            tavern_pointers.append('/histories/'+str(i))
    check('Tavern/reused-paid-histories-present',len(tavern_pointers)>=4)
    for b in tavern['sourceBindings']:check('Tavern/reused-input-current/'+b['path'],info(G/b['path'])==b)
    generic=read(paths[14]);check('existing-immutable-training-vision-evidence-pass',not generic['failures'])
    reused_results=[]
    for i,row in enumerate(generic['results']):
        label=row.get('id',row.get('name',''))
        if any(x in label for x in ['later proficiency is not automatic Expertise','independent Expertise is strongest','Two skill snapshots','prior vision','extension30','Base branch never']):
            check('existing-generic/'+str(i),row['pass']);reused_results.append('/results/'+str(i))
    check('existing-training-boundaries-actually-joined',len(reused_results)>=10)
    for sid in group['exactMembers']:
        pointers=['/histories/'+str(i) for i,x in enumerate(histories) if x.get('feat')==sid or sid in x.get('feats',[])]
        check(sid+'/has-actual-paid-descriptor-binding',bool(pointers) or sid=='tavern_brawler' and bool(tavern_pointers))
        descriptor_rows.append({'id':sid,'completeContract':deepcopy(contracts[sid]),
            'gptMandatorySelectionsAndSnapshots':deepcopy(rows[sid]['b_mandatorySelectionsAndSnapshots']),
            'gptInitialState':deepcopy(rows[sid]['c_initialState']),
            'freshPaidHistoryPointers':pointers,'reusedPaidEvidence':{'report':info(paths[13]),'pointers':tavern_pointers} if sid=='tavern_brawler' else None,
            'fullUseRuntimeImplemented':False})
    check('all-source-bindings-unchanged',[info(p) for p in paths]==bindings)
    stamp=datetime.now(timezone.utc).isoformat()
    desc.write_text(json.dumps({'recordedAtUtc':stamp,'scope':'Exact21 FW07 descriptor/paid-commit/source snapshot join; no full feat-use or campaign proof.',
        'sourceBindings':bindings,'entries':descriptor_rows},indent=2,ensure_ascii=False,default=serial)+'\n',encoding='utf-8')
    result={'recordedAtUtc':stamp,'status':'pass','checks':len(checks),'failures':[],'acceptanceGroups':['AA-16'],'finiteWorkGroup':'FW-07',
        'exactDescriptorCount':21,'historyCount':len(histories),'sourceBindings':bindings,'descriptors':info(desc),'results':checks,'histories':histories,
        'reusedEvidence':{'TavernBrawler':{'report':info(paths[13]),'pointers':tavern_pointers},
            'fixedTrainingAndVision':{'report':info(paths[14]),'pointers':reused_results}},
        'scope':'Fixed-versus-live snapshot, exact recipient and duplicate branch assembly. Actual paid histories are synthetic source-qualified slices; conditional suppression/independent-source/level-loss inputs are not campaign events.',
        'newGameRules':0,'sourceInformationDeleted':0,'fullFeatCandidateApproved':False}
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,default=serial)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(out),'descriptors':info(desc)}))


if __name__=='__main__':main()
