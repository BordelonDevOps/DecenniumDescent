"""Source-bound paid-copy and CRS lifecycle checks; no whole-engine claim.

Run without arguments for repeatable verification. --write-report saves one
new immutable report and refuses to overwrite successful prior evidence.
"""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import sys
from feat335_copy_capture import CopyAcquisition, CopyCaptures
from feat335_copy_source_components import CopySourceComponents
from feat335_copy_release import CopyReleases, CopyConcentration, copy_quote, CONCENTRATION
from feat_exact_01_casting_credential_model import CastingSources
from transformation_spell_playtest_rules import ConcentrationLedger
from spell_playtest_rules import quote_cast
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT335_COPY_RELEASE_01_CHECK.json'
    write = sys.argv[1:] == ['--write-report']
    if sys.argv[1:] and not write: raise ValueError('Use --write-report or no arguments')
    if write: assert not output.exists(), 'Preserve prior successful evidence'
    paths = [R/'data/playtest/character_foundation.json', R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json', R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json', R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        A/'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json',
        A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json',
        A/'FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',
        R/'docs/mechanics/SPELL_INTEGRATION_RULES.md', R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
        Path(__file__), *[R/'tools'/n for n in ['feat335_copy_release.py','feat335_copy_capture.py',
        'feat335_copy_source_components.py','feat_exact_01_composite_casting_model.py',
        'feat_exact_01_casting_credential_model.py','feat_exact_01_acquisition_models.py',
        'feat_exact_01_training_prerequisite_model.py','transformation_spell_playtest_rules.py','spell_playtest_rules.py']]]
    foundation, ancestry, equipment, sm, deps, wizard, contracts, prior, source_report, addendum = [read(p) for p in paths[:10]]
    for dep in deps['spells'].values():
        p = G / dep['binding']['file']
        if p not in paths: paths.append(p)
    bindings = [info(p) for p in paths]
    classes = {x['class']:x for x in foundation['classes']}
    skills = {s:a for a,ss in foundation['skillAbilities'].items() for s in ss}
    equipment = {x['id']:x for x in equipment['records']}
    backgrounds = {x['id']:x for x in ancestry['backgrounds']}
    supplements = {x['id']:x['value'] for x in sm['groups']}
    contracts = {x['id']:x for x in contracts['records']}
    sources = CastingSources(G, deps['spells'], supplements, wizard)
    checks=[]; histories=[]
    def check(label, ok):
        checks.append({'id':label,'passed':bool(ok)})
        assert ok, label
    def reject(label, model, fn, frame=None):
        before=model.snapshot(); f=deepcopy(frame)
        try: fn()
        except ValueError: check(label,True)
        else: check(label,False)
        check(label+'/atomic',before==model.snapshot() and f==frame)
    def record(label,m):
        histories.append({'id':label,'state':m.snapshot(),'acquisition':m.captures.acquired.snapshot(),
                          'sourceWitnesses':m.captures.witnesses.snapshot()})
    geometry=dict(actualCaptureWindow=True,conscious=True,actualFeatAvailable=True,sourceCreatureDistance=30,
        resolvedComponentDistance=30,sourcePerceived=True,effectPerceived=True,lineOfEffect=True,
        usedAgainstOwner=False,sourceLawfulRange=True,actualReactionLegal=True)
    def make(first='Wizard', feats=('eldritch_echo','mimicry','arcane_adaptation')):
        actor=deepcopy(prior['actorSourceProjection'])
        actor.update(firstClass=first,classLevels={first:1},selectedClassSkills=['Insight','Investigation'] if first=='Wizard' else ['Nature','Athletics'])
        h=CopyAcquisition(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources)
        h.advance(4)
        if first=='Wizard':h.wizard(['arcane-ray','friends'],['find-familiar'],['find-familiar'])
        else:h.earn(4);h.acquire_parent('forbidden_pact',4,{'sigil':'hex'})
        for sid,level in zip(feats,[4,8,12] if first=='Wizard' else [8,12,16]):
            h.advance(level);h.earn(level);h.acquire_copy(sid,level)
        w=CopySourceComponents(sources)
        for row in source_report['histories']:
            if row['id'].startswith('all-seven/'):
                for event,s in row['state'].items():
                    w.witness(event,s['spellId'],s['sourceRoute']['sourceClass'],s['sourceClassLevel'],s['premises'],s['outcome'])
        c=CopyCaptures(h,w)
        maximum=wizard['rpByClassLevel'][h.pay.current_classes['Wizard']-1] if first=='Wizard' else 0
        pool=dict(owner='owner',source='Wizard/class-engine' if first=='Wizard' else 'no-acquired-RP-pool',rp=maximum,maxRP=maximum)
        cadence=dict(dissonance=0,previousSpell=None,refrain=0,classRecords={'unrelated-record':'preserved'})
        return CopyReleases(c,'owner',pool,cadence,ConcentrationLedger())
    def capture(m,event='capture',profile='burst',sid='mimicry',adapt=False,source=None,provider='Wizard/class-engine',replace=False):
        return m.captures.capture(event,sid,source or 'source-'+profile,profile,provider,deepcopy(geometry),adapt=adapt,replace=replace)
    def start(m,ordinal=1,round_=1):
        c=m.captures
        if c.current_turn:
            if c.current_kind=='regular':c.end_regular(c.current_turn,actual_regular_end=True)
            else:c.end_extra(c.current_turn,actual_extra_end=True)
        c.start_regular('turn'+str(ordinal),ordinal,round_,actual_new_regular_start=True)
    def frame(m):
        return dict(turn=m.captures.current_turn,round=m.captures.current_round,actions=1,conscious=True,canAct=True,
                    verbal=True,somatic=True,magicAllowed=True,knownLegalSelection=True,unmodifiedPrice=True,ordinaryActionAllowed=True)
    def cast(m,event='cast',cap='capture',permission='pending',provider='Wizard/class-engine',f=None):
        return m.commit(event,cap,permission=permission,grant_id=provider,frame=frame(m) if f is None else f)
    profiles=supplements['SUP-07']['copyProfileContract']['profiles']
    check('actual-applied-CRS-profile-tags',{x['id']:x['concentrationRequired'] for x in profiles}==CONCENTRATION)

    # Every profile crosses acquisition -> actual captured component -> paid cast.
    for profile in CONCENTRATION:
        m=make();capture(m,profile=profile);start(m);f=frame(m);old=[]
        m.lifecycle.ledger.start_committed('owner','prior-real-concentration',lambda reason:old.append(reason))
        p=cast(m,f=f)
        expected=0 if profile=='strike' else 2
        check(profile+'/paid',m.pool['rp']==44-expected and f['actions']==0 and m.captures.pending is None)
        check(profile+'/history',m.cadence['dissonance']==(0 if profile=='strike' else 1) and p['quote']['refrain']==0)
        check(profile+'/commit-concentration',bool(old)==CONCENTRATION[profile])
        m.lifecycle.after_counter_window('cast',countered=False,effect_established=CONCENTRATION[profile])
        check(profile+'/concentration-preserved-or-replaced',m.lifecycle.snapshot()['currentBurden']==('cast' if CONCENTRATION[profile] else 'prior-real-concentration'))
        check(profile+'/no-proc-or-repertoire',not p['classProcAllowed'] and not p['newRepertoire'] and not p['furtherCaptureAllowed'])
        if CONCENTRATION[profile]:
            m.lifecycle.ledger.end('owner','actual-failed-concentration')
            check(profile+'/immediate-lifecycle-cleanup',not m.lifecycle.casts['cast']['effectActive'] and m.lifecycle.casts['cast']['endReason']=='actual-failed-concentration')
        record('seven-profile/'+profile,m)
    for profile in ['ward','hindrance','boon']:
        m=make();capture(m,profile=profile);start(m);ended=[]
        m.lifecycle.ledger.start_committed('owner','old',lambda why:ended.append(why));before=m.pool['rp']
        cast(m);m.lifecycle.after_counter_window('cast',countered=True)
        check(profile+'/counter-no-refund-or-restoration',m.pool['rp']==before-2 and ended==['new-concentration'] and not m.lifecycle.ledger.current and m.captures.pending is None and m.cadence['dissonance']==1)
        reject(profile+'/no-repeat-counter',m,lambda:m.lifecycle.after_counter_window('cast',countered=True))
        record('counter/'+profile,m)

    # Lifedraw has two genuinely observed components: changing profile cannot
    # manufacture a fresh source family. The second cast uses paid Adaptation.
    m=make();capture(m,profile='strike',source='source-mend',adapt=True);start(m)
    first=cast(m);m.lifecycle.after_counter_window('cast',countered=False)
    reject('same-numbered-round-cap',m,lambda:cast(m,'again',permission='adapted'))
    # A future extra turn in the SAME round cannot refresh the shared allowance.
    m.captures.end_regular('turn1',actual_regular_end=True);m.captures.start_extra('extra',1,actual_extra_turn=True)
    reject('extra-turn-no-new-release',m,lambda:cast(m,'extra-copy',permission='adapted'))
    m.captures.end_extra('extra',actual_extra_end=True)
    m.captures.start_extra('next-round-extra',2,actual_extra_turn=True)
    second=cast(m,'adapted-copy',permission='adapted')
    check('CRS01-B/actual-adapted-cast-shares-history',first['quote']['castFamilyKey']==second['quote']['castFamilyKey']=='feat-copy::lifedraw' and second['quote']['refrain']==1 and m.cadence['dissonance']==3 and m.pool['rp']==40)
    m.lifecycle.after_counter_window('adapted-copy',countered=False)
    start(m,2,3)
    reject('adaptation-expires-at-second-future-start',m,lambda:cast(m,'expired',permission='adapted'))
    record('actual-adapted-chronology',m)

    # A separate captured profile of the SAME actual source still repeats.
    m=make();capture(m,profile='strike',source='source-mend');start(m);cast(m)
    m.lifecycle.after_counter_window('cast',countered=False)
    capture(m,'second',profile='mend',source='source-mend',sid='eldritch_echo');start(m,2,2)
    p=cast(m,'second-cast','second')
    check('CRS01-A/changed-capture-profile-feat-same-family',p['quote']['refrain']==1 and m.cadence['dissonance']==3)
    record('actual-different-profile-same-source',m)
    m=make();capture(m,profile='strike');start(m);cast(m);m.lifecycle.after_counter_window('cast',countered=False)
    capture(m,'second',profile='strike',source='source-mend',sid='eldritch_echo');start(m,2,2)
    p=cast(m,'second-cast','second')
    check('CRS01-D/different-sources-same-strike',p['quote']['refrain']==0 and m.cadence['previousSpell']=='feat-copy::lifedraw')
    record('actual-different-source-same-profile',m)

    # Ordinary known Arcane Ray uses quote_cast's ordinary family. This tests
    # the common quotation boundary, not a separate full ordinary cast engine.
    m=make();capture(m,profile='strike');start(m)
    ordinary=quote_cast(sources.dependencies['arcane-ray']['completeCurrentProcedureCard'],'Wizard',12,
        available_spell_ids={'arcane-ray'},rp=44,max_rp=44,dissonance=0,proficiency=4,casting_modifier=3)
    m.cadence.update(previousSpell=ordinary['spellId'],refrain=ordinary['refrain'],dissonance=ordinary['dissonanceBeforeClassInterface'])
    p=cast(m)
    check('CRS01-C/ordinary-family-separate',p['quote']['castFamilyKey']=='feat-copy::arcane-ray' and p['quote']['refrain']==0)
    record('ordinary-quotation-boundary',m)

    # Independent FS-09 boundaries use explicit operands, not a fabricated
    # Shaman/Mirrorsage acquisition. Missing class adapters remain open below.
    component=make().captures.witnesses.select('source-burst','burst')
    pool=dict(rp=20,maxRP=20);cadence=dict(dissonance=0,previousSpell=None,refrain=0)
    q=copy_quote(component,proficiency=3,modifier=3,pool=pool,cadence=cadence)
    ordinary=quote_cast(sources.dependencies['burning-hands']['completeCurrentProcedureCard'],'Wizard',5,
        available_spell_ids={'burning-hands'},rp=20,max_rp=20,dissonance=0,proficiency=3,casting_modifier=3)
    check('CRS03-D/scoped-Limits',q['limit']==9 and ordinary['limit']==8)
    for d,cost in [(8,2),(9,3),(11,3),(12,4),(14,4)]:
        q=copy_quote(component,proficiency=3,modifier=3,pool=pool,cadence={**cadence,'dissonance':d})
        check('price-boundary/'+str(d),q['cost']==cost)
    q=copy_quote(component,proficiency=2,modifier=-5,pool=pool,cadence=cadence)
    check('minimum-feat-Limit',q['limit']==4)
    for previous, expected in [(0,1),(1,2),(2,3),(3,3)]:
        q=copy_quote(component,proficiency=3,modifier=3,pool=pool,
            cadence={**cadence,'previousSpell':'feat-copy::burning-hands','refrain':previous})
        check('ordinary-Refrain-cap/'+str(previous),q['refrain']==expected and q['dissonanceAdded']==1+expected)
    for bad in [{**component,'sourceSpellId':''},{**component,'sourceSpellId':None},
                {**component,'copyRank':2},{**component,'originalRank':True}]:
        try:copy_quote(bad,proficiency=3,modifier=3,pool=pool,cadence=cadence)
        except ValueError:check('invalid-source-or-rank/'+str(len(checks)),True)
        else:check('invalid-source-or-rank',False)
    m=make();capture(m);start(m)
    m.cadence['classRecords'].update(wizardPreparedMatrixUnused=True,shamanVentAvailable=True,mirrorsageFirstReleaseWaiver=True)
    old=deepcopy(m.cadence['classRecords']);p=cast(m)
    check('CRS03-A/actual-Wizard-no-exemption',p['quote']['baseDissonance']==1 and p['quote']['dissonanceAdded']==1 and m.cadence['classRecords']==old)
    record('Wizard-independent-strain',m)
    # Later nested history must survive the parent's eventual outcome.
    m=make();capture(m);start(m);cast(m)
    m.cadence.update(previousSpell='actual-nested-spell-fixture',refrain=2,dissonance=7)
    nested=deepcopy(m.cadence);m.lifecycle.after_counter_window('cast',countered=True)
    check('parent-resumption-keeps-nested-chronology',m.cadence==nested and m.pool['rp']==42)
    record('counter-outcome-never-rewinds-history',m)

    # Every isolated rejection must preserve costs, permission, action, cadence
    # and prior concentration. Declarations with modifiers fail closed.
    for key in ['conscious','canAct','verbal','somatic','magicAllowed','knownLegalSelection','unmodifiedPrice','ordinaryActionAllowed']:
        m=make();capture(m);start(m);f=frame(m);f[key]=False
        reject('preflight/'+key,m,lambda:cast(m,f=f),f)
    m=make();capture(m);start(m);m.pool['rp']=1;f=frame(m)
    reject('insufficient-RP',m,lambda:cast(m,f=f),f)
    m=make();capture(m);start(m);f=frame(m);f['actions']=0
    reject('spent-Action',m,lambda:cast(m,f=f),f)
    m=make();capture(m);start(m);m.pool['source']='new-copy-pool'
    reject('cannot-create-copy-RP-pool',m,lambda:cast(m))
    m=make();capture(m);start(m);m.cadence['dissonance']=max(4,8+(m.captures.acquired.pay.scores['INT']-10)//2)+6
    reject('Fractured-ranked-block',m,lambda:cast(m))
    m=make();capture(m);start(m);m.captures.acquired.remove_personal_routes()
    reject('removed-provider-at-release',m,lambda:cast(m))
    m=make();capture(m);start(m);m.captures.acquired.pay.suppress('mimicry')
    reject('suppressed-copy-feat-at-release',m,lambda:cast(m))
    m=make();capture(m);start(m);m.captures.pending['component']['sourceSpellId']='invented-key'
    reject('cannot-forge-favorable-family',m,lambda:cast(m))
    m=make();capture(m,sid='eldritch_echo');start(m);start(m,2,2)
    reject('Echo-expired-window',m,lambda:cast(m))
    for provider in ['Shaman/class-engine','Mirrorsage/class-engine']:
        m=make();capture(m);start(m)
        reject('unsupported-provider/'+provider,m,lambda:cast(m,provider=provider))

    m=make(first='Warrior');pact=next(k for k,g in m.captures.acquired.casting.grants.items() if g['source']=='actual-paid-Forbidden-Pact')
    echo=next(k for k,g in m.captures.acquired.casting.grants.items() if g['source']=='actual-paid-Eldritch-Echo')
    capture(m,profile='strike',provider=pact,adapt=True);start(m);p=cast(m,provider=echo)
    check('CRS03-E/paid-feat-only-q0-CHA-no-pool',p['provider']['ability']=='CHA' and p['provider']['maximumLearnableRank']==0 and m.pool['rp']==m.pool['maxRP']==0 and p['quote']['rank']==0)
    m.lifecycle.after_counter_window('cast',countered=False)
    reject('CRS03-E/q1-ineligible',m,lambda:capture(m,'ranked',provider=echo,sid='eldritch_echo'))
    record('actual-feat-only-route',m)
    m=make(first='Warrior');pact=next(k for k,g in m.captures.acquired.casting.grants.items() if g['source']=='actual-paid-Forbidden-Pact')
    capture(m,profile='strike',provider=pact);start(m)
    m.cadence.update(previousSpell='feat-copy::arcane-ray',refrain=3,dissonance=100)
    p=cast(m,provider=pact)
    check('Fractured-q0-still-casts-with-Refrain',p['quote']['cost']==0 and p['quote']['refrain']==3 and m.cadence['dissonance']==103 and m.pool['maxRP']==0)
    record('rank0-Fractured-history',m)
    # Two real owned routes, same actual q0 source, no history reset.
    m=make();capture(m,profile='strike',adapt=True);start(m);cast(m);m.lifecycle.after_counter_window('cast',countered=False)
    m.captures.end_regular('turn1',actual_regular_end=True);m.captures.start_extra('round2extra',2,actual_extra_turn=True)
    echo=next(k for k,g in m.captures.acquired.casting.grants.items() if g['source']=='actual-paid-Eldritch-Echo')
    p=cast(m,'CHA-copy',permission='adapted',provider=echo)
    check('CRS01-B/actual-INT-to-CHA-route',p['quote']['refrain']==1 and p['provider']['ability']=='CHA')
    record('actual-route-change-retains-chronology',m)

    # Ready concentration only. Payment/scheduler/cap are explicitly not
    # integrated; a committed preparation is the input boundary here.
    ready_histories=[]
    for profile in CONCENTRATION:
        ledger=ConcentrationLedger();life=CopyConcentration('owner',ledger,profiles);ended=[]
        ledger.start_committed('owner','old',lambda why:ended.append(why))
        life.committed('paid-ready',profile,ready=True)
        check('CRS02-D/'+profile+'/setup-one-slot',ended==['new-concentration'] and len(ledger.current)==1)
        life.after_counter_window('paid-ready',countered=False)
        before=ledger.current['owner'];life.release_ready('paid-ready',actual_legal_release=True,effect_established=CONCENTRATION[profile])
        check('CRS02-D/'+profile+'/release-same-or-end',ledger.current.get('owner')==before if CONCENTRATION[profile] else not ledger.current)
        if CONCENTRATION[profile]:
            life.end_at_deadline('paid-ready',actual_source_deadline=True)
            check('ready/'+profile+'/deadline-cleanup',not ledger.current and not life.casts['paid-ready']['effectActive'])
        ready_histories.append(life.snapshot())
    life=CopyConcentration('owner',ConcentrationLedger(),profiles)
    life.committed('paid','ward');life.ledger.end('owner','nested-concentration-loss')
    life.after_counter_window('paid',countered=False)
    check('concentration-lost-inside-counter-window-no-restoration',life.casts['paid']['state']=='ended' and not life.ledger.current)
    life=CopyConcentration('owner',ConcentrationLedger(),profiles)
    life.committed('paid-ready','strike',ready=True);life.after_counter_window('paid-ready',countered=False)
    life.ledger.end('owner','lost-before-trigger');before=life.snapshot()
    try:life.release_ready('paid-ready',actual_legal_release=True)
    except ValueError:check('lost-Ready-cannot-release',life.snapshot()==before)
    else:check('lost-Ready-cannot-release',False)
    check('source-bytes-preserved',bindings==[info(p) for p in paths])
    coverage=[]
    for e in addendum['acceptanceExamples']:
        id_=e['id']
        status='bounded-interface-tested'
        limitations=[]
        if id_ in {'CRS03-B','CRS03-C'}:
            status='open-class-provider-integration'
            limitations=['Unsupported actual class routes reject; no Shaman totem or Mirrorsage shared allowance engine executed.']
        if id_=='CRS01-A':limitations=['Different actual capture/profile/feat tested; two Echo captures across a real beneficial rest and varying same-source class rank are not executed.']
        if id_=='CRS01-C':limitations=['Ordinary quote/history boundary tested; no full ordinary spell cast/payload transaction here.']
        if id_=='CRS02-D':limitations=['Shared concentration lifecycle tested from paid-preparation premise; Ready payment, trigger, Reaction, expiry scheduling and release cap remain unintegrated.']
        coverage.append({**e,'status':status,'limitations':limitations})
    report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'results':checks,'histories':histories,'readyLifecycleHistories':ready_histories,
        'acceptanceCoverage':coverage,'newRuleDecisions':0,
        'scope':'Actual paid copy acquisitions and conditional witnessed source components connect to direct-Action payment, RP/cadence, permission consumption, owner-round cap, current provider and shared concentration. Separate Ready lifecycle boundary exercised.',
        'limits':['World source completion, perception, capture geometry, action frames, selection legality and magic/component predicates remain conditional scenario premises.',
        'Only the actual Wizard and paid rank-zero Blast credential routes are connected. Shaman/Mirrorsage and other providers, shared class release caps and priced modifiers are not implemented.',
        'Recipient HP/damage/healing/movement/buffer/control effects, real world deadlines, suppression/dispel, save-load and live engine behavior are not executed by this release adapter.',
        'Concentration effectActive is a lifecycle record, not evidence of an actual recipient modifier or successful target resolution.',
        'Ready starts from already-paid preparation; no complete Ready transaction or owner-round cap timing is claimed.',
        'Source-bound finite tests do not approve the 335 feats, numerical balance, human gameplay, cosmology canon, publication or whole game.'],
        'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'wholeGameComplete':False}
    if write:output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'acceptanceRows':len(coverage),'openClassProviderRows':2,'report':info(output) if write else None}))


if __name__=='__main__':main()
