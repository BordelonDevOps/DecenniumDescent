"""Source-bound finite witnesses; no copy feat acquisition or release claim."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from feat335_copy_source_components import CopySourceComponents, bounded_native_numeric
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def main():
    output=A/'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json';assert not output.exists()
    paths=[R/'data/public/feat_candidates/exact_01/spell_dependencies.json',
        R/'data/public/feat_candidates/exact_01/supplements.json',R/'data/public/class_playtests/wizard.json',
        R/'tools/feat335_copy_source_components.py',R/'tools/feat_exact_01_casting_credential_model.py',Path(__file__)]
    bindings=[info(p) for p in paths];deps,sm,wizard=[read(p) for p in paths[:3]]
    supplements={x['id']:x['value'] for x in sm['groups']}
    sources=CastingSources(G,deps['spells'],supplements,wizard)
    checks=[];histories=[]
    def check(label,ok):
        checks.append({'id':label,'passed':bool(ok)});assert ok,label
    def reject(label,m,fn):
        before=m.snapshot()
        try:fn()
        except ValueError:check(label,True)
        else:check(label,False)
        check(label+'/no-mutation',m.snapshot()==before)
    premises={'resolved':True,'directlyWitnessed':True,'actualLegalSourceCast':True,'copyDerived':False,'protectedFeature':False}
    fixtures=[('strike','arcane-ray',1,{'actualHit':True,'ordinaryNativeDice':[6]},0,6),
        ('burst','burning-hands',1,{'ordinaryNativeDice':[6,5,4],'actualResolvedArea':True},1,15),
        ('mend','lifedraw',1,{'actualHit':True,'ordinaryNativeDice':[6,6,6],'actualNecroticDamageDealt':10,'targetCategory':'living-hostile'},1,5),
        ('ward','false-life',1,{'ordinaryNativeDice':[4],'actualWillingLivingRecipient':True},1,8),
        ('hindrance','slow',5,{'actualFailedSave':True,'actualSurvivingControlComponent':True,'mode':'Enchantment'},1,None),
        ('boon','shield',1,{'actualAcBenefitEstablished':True},1,None),
        ('step','mist-step',1,{'observedDistance':30,'actualLegalTeleportCompleted':True},1,None)]
    for profile,sid,level,outcome,q,magnitude in fixtures:
        m=CopySourceComponents(sources);r=m.witness('source-'+profile,sid,'Wizard',level,premises,outcome)
        selected=m.select('source-'+profile,profile)
        check(profile+'/reviewed-whole-card-and-exact-placement',selected['sourcePayloadBinding']==deps['spells'][sid]['binding'] and r['originalRank']==deps['spells'][sid]['originalCatalogRecord']['classAccess']['Wizard']['rank'])
        check(profile+'/derived-rank-no-capture-or-release',selected['copyRank']==q and not selected['captureAuthorized'] and not selected['releaseExecuted'])
        if magnitude is not None:
            check(profile+'/native-before-recipient-cap',selected['nativeMagnitude']==magnitude)
            check(profile+'/half-native-cap',bounded_native_numeric(selected,[6]*(q+1))==magnitude//2)
            check(profile+'/low-copy-roll-cap',bounded_native_numeric(selected,[1]*(q+1))==min(q+1,magnitude//2))
            for roll in [[6]*q,[7]*(q+1),[True]*(q+1)]:
                reject(profile+'/invalid-copy-dice/'+str(roll),m,lambda roll=roll:bounded_native_numeric(selected,roll))
        else:reject(profile+'/not-numeric',m,lambda:bounded_native_numeric(selected,[1,1]))
        if profile=='boon':check('shield-only-benefits-AC-not-save-or-attack',selected['benefitedStatistics']==['AC'])
        if profile=='step':check('mist-step-actual30-produces15-ceiling',min(15,selected['observedDistance']//2)==15 and selected['wasTeleport'])
        for other in {'strike','burst','mend','ward','hindrance','boon','step'}-{c['profile'] for c in r['components']}:
            reject(profile+'/does-not-invent-'+other,m,lambda other=other:m.select('source-'+profile,other))
        reject(profile+'/canonical-event-no-replay',m,lambda:m.witness('source-'+profile,sid,'Wizard',level,premises,outcome))
        histories.append({'id':'all-seven/'+profile,'state':m.snapshot(),'selected':selected})
    check('all-seven-source-witnessed-profiles', {x[0] for x in fixtures}=={x['id'] for x in supplements['SUP-07']['copyProfileContract']['profiles']})

    m=CopySourceComponents(sources)
    for field in premises:
        bad=deepcopy(premises);bad[field]=not bad[field]
        reject('source-event-gate/'+field,m,lambda bad=bad:m.witness('bad','arcane-ray','Wizard',1,bad,fixtures[0][3]))
    reject('actual-source-class-placement-required',m,lambda:m.witness('bad','arcane-ray','Ranger',1,premises,fixtures[0][3]))
    reject('source-actual-class-level-required',m,lambda:m.witness('bad','slow','Wizard',4,premises,fixtures[4][3]))
    reject('source-level-not-bool',m,lambda:m.witness('bad','arcane-ray','Wizard',True,premises,fixtures[0][3]))
    reject('no-arbitrary-native-B',m,lambda:m.witness('bad','arcane-ray','Wizard',1,premises,{'actualHit':True,'ordinaryNativeDice':[6],'nativeMagnitude':900}))
    for sid in ['seal-minor-wound','false-comfort','mending','spare-the-dying','flickerstep']:
        reject('name-or-apparent-healing-not-authority/'+sid,m,lambda sid=sid:m.witness('bad',sid,'Wizard',20,premises,{}))
    for sid in ['seal-minor-wound','false-comfort','mending','spare-the-dying']:
        sources.ordinary(sid,'Wizard')
        op=deps['spells'][sid]['completeCurrentProcedureCard']['operational']
        check('source-non-healing/'+sid,any(s in json.dumps(op).lower() for s in ['restores no hp','restore device or construct hp']))
    histories.append({'id':'source-gate-isolation','state':m.snapshot()})

    for category in ['living-hostile','undead','construct','farmed-summon','ally','helpless-captive','corpse','other-nonliving']:
        m=CopySourceComponents(sources);o=deepcopy(fixtures[2][3]);o['targetCategory']=category
        r=m.witness('life','lifedraw','Wizard',1,premises,o)
        check('lifedraw-healing-eligibility/'+category,('mend' in [c['profile'] for c in r['components']])==(category=='living-hostile'))
        if category!='living-hostile':reject('no-healing-component/'+category,m,lambda:m.select('life','mend'))
        histories.append({'id':'lifedraw/'+category,'state':m.snapshot()})
    for actual in [0,1,2,9,10,17,18]:
        m=CopySourceComponents(sources);o=deepcopy(fixtures[2][3]);o['actualNecroticDamageDealt']=actual
        r=m.witness('life','lifedraw','Wizard',1,premises,o)
        if actual:
            selected=m.select('life','mend')
            check('lifedraw-native-heal-derived-from-actual-damage/'+str(actual),selected['nativeMagnitude']==actual//2)
            check('lifedraw-copy-half-heal-not-half-source-damage/'+str(actual),bounded_native_numeric(selected,[6,6])==(actual//2)//2)
        else:reject('zero-damage-no-heal',m,lambda:m.select('life','mend'))
        histories.append({'id':'lifedraw-damage/'+str(actual),'state':m.snapshot()})
    for sid in ['arcane-ray','lifedraw']:
        m=CopySourceComponents(sources);o={'actualHit':False,'ordinaryNativeDice':[]}
        if sid=='lifedraw':o.update(actualNecroticDamageDealt=0,targetCategory='living-hostile')
        r=m.witness('miss',sid,'Wizard',1,premises,o)
        check('miss-no-source-component/'+sid,r['components']==[])
        reject('miss-cannot-copy-damage/'+sid,m,lambda:m.select('miss','strike'))
        histories.append({'id':'actual-miss/'+sid,'state':m.snapshot()})
    for failed,surviving in [(False,True),(True,False),(False,False)]:
        m=CopySourceComponents(sources)
        r=m.witness('slow','slow','Wizard',5,premises,{'actualFailedSave':failed,'actualSurvivingControlComponent':surviving,'mode':'Enchantment'})
        check('no-expressed-control/'+str((failed,surviving)),not r['components'])
        histories.append({'id':'slow-negative/'+str((failed,surviving)),'state':m.snapshot()})
    m=CopySourceComponents(sources)
    reject('slow-no-mode-union',m,lambda:m.witness('slow','slow','Mage',5,premises,fixtures[4][3]))
    r=m.witness('slow','slow','Mage',5,premises,{**fixtures[4][3],'mode':'Transmutation'})
    check('actual-Mage-mode-also-hindrance',r['components']==[{'profile':'hindrance'}])
    histories.append({'id':'actual-transmutation-slow','state':m.snapshot()})
    for distance in [0,1,5,10,29,30]:
        m=CopySourceComponents(sources);m.witness('step','mist-step','Wizard',1,premises,{'observedDistance':distance,'actualLegalTeleportCompleted':True})
        selected=m.select('step','step')
        check('step-actual-distance-not-printed-range/'+str(distance),min(15,selected['observedDistance']//2)==distance//2)
        histories.append({'id':'actual-teleport-distance/'+str(distance),'state':m.snapshot()})
    for distance in [-1,31,True]:
        reject('impossible-source-teleport/'+str(distance),m,lambda distance=distance:m.witness('bad','mist-step','Wizard',1,premises,{'observedDistance':distance,'actualLegalTeleportCompleted':True}))
    source_files={v['sourceRoute']['payloadBinding']['file'] for h in histories for v in h['state'].values()}
    bindings.extend(info(G/f) for f in sorted(source_files))
    check('all-source-bindings-stable',all(info(G/b['path'])==b for b in bindings))
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'completeCopyContract':supplements['SUP-07']['copyProfileContract'],
        'results':checks,'histories':histories,'counts':{'conditionalHistories':len(histories),'profiles':7,'positiveSpellSources':7},
        'scope':'Exact whole-card source bindings and actual class placement feed seven finite component witnesses. Native damage/ward dice, Lifedraw qualifying damage-to-heal derivation, actual Slow mode/result, Shield AC-only and completed Mist Step distance constrain profile selection and native numeric bounds.',
        'limits':['Source-cast payment, repertoire, attack/save/defense resolution, direct perception, actual world geometry and completion are supplied conditional premises; this adapter cannot authenticate a campaign occurrence.',
            'Only seven explicitly named ordinary source procedures are modeled. Rejection of unadapted sources is scope restriction, not a general game ruling that they can never qualify. The separately bound non-healing examples support their specific negative interpretations.',
            'Selecting a witness neither spends nor authorizes capture. Paid Echo/Mimicry/Adaptation acquisition, qualifying own rank route, timing/Reaction/use/rest/copy-record lifecycle and full paid release/counter/casting history remain required.',
            'Native ordinary damage dice exclude external add-ons and separately copied critical multipliers. Actual Lifedraw damage after its own defenses is a premise and is used only to derive the original healing component before the healer maximum/other recipient limits.',
            'No full recipient damage/healing/ward/control/boon/movement application, monster effective rank, protected-feature exception or Mirrorsage engine is executed.',
            'No source-rule adoption, full335 approval, runtime certification, human balance evidence, GitHub push or cosmology review follows.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(output)}))


if __name__=='__main__':main()
