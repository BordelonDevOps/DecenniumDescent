"""Promote only the actually closed five-spell scope, preserving all originals."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,subprocess,sys
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
IDS={'harmonic-bulwark','polymorph','shapechange','true-polymorph','mass-polymorph'}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
reply=(HERE/'GPT_TRANSFORMATION_CORRECTION_AND_FEAT_REVIEW.md').read_text(encoding='utf-8')
head,feats=reply.split('Eight-feat source conference',1)
assert 'I find no remaining reproducible blocker' in head and 'Eligible for provisional catalog promotion' in head
assert '216 contract checks' in head and '729' in head and 'REVIEWED / reference-VALIDATED' in head
closure_path=HERE/'GPT_TRANSFORMATION_SPELL_FINAL_CLOSURE.md'
closure_text='# GPT confirmed five-spell bounded closure\n\n'+head.split('ChatGPT said:',1)[1].strip()+'\n'
if closure_path.exists():assert closure_path.read_text(encoding='utf-8')==closure_text
else:closure_path.write_text(closure_text,encoding='utf-8')
(HERE/'GPT_BUFFER_FEAT_FIRST_REVIEW.md').write_text('# GPT eight-feat first full-clause proposals\n\nEight-feat source conference'+feats,encoding='utf-8')
closure=closure_path.relative_to(GAME).as_posix()
closure_hash=hashlib.sha256(closure_path.read_bytes()).hexdigest()
draft=read(ROOT/'data/playtest/spell_drafts/candidate_transformations.json')
assert {s['id'] for s in draft['spells']}==IDS
for s in draft['spells']:
    s['implementationStatus']='REVIEWED / reference-VALIDATED operational-playtest draft'
    s['reviewEvidence']=[closure]
batch={'status':'REVIEWED / reference-VALIDATED operational-playtest drafts','scope':'Five bounded spell interfaces; not numerical balance or whole-game certification',
       'reviewEvidence':[closure],'spells':draft['spells']}
batchpath=ROOT/'data/playtest/spell_drafts/batch_transformations.json'
if batchpath.exists():assert read(batchpath)==batch
else:write(batchpath,batch)
groups=read(ROOT/'data/playtest/spell_drafts/selected_sources.json')
for ident in sorted(IDS):
    group='Universal' if ident=='harmonic-bulwark' else 'Transmutation'
    if ident not in groups[group]:groups[group].append(ident)
write(ROOT/'data/playtest/spell_drafts/selected_sources.json',groups)
run=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/build_spell_playtests.py')],capture_output=True,text=True,encoding='utf-8')
print(run.stdout.strip());assert run.returncode==0,run.stderr
current={s['id']:s for s in read(ROOT/'data/public/spell_playtests/catalog.json')['spells']}
historical=read(HERE/'FORM_TEMP_HP_CONFERENCE_SOURCES.json')
evolution={}
for old in historical['records']:
    if old['kind']!='ordinary-spell' or old['sourceId'] not in IDS:continue
    ident=old['sourceId'];after=current[ident];before=old['overlayObject'];mutable={'status','operational','reviewFlags'}
    assert {k:v for k,v in before.items() if k not in mutable}=={k:v for k,v in after.items() if k not in mutable}
    assert digest(before)==old['overlayObjectSha256']
    evolution[ident]={'oldOverlaySha256':digest(before),'newOverlaySha256':digest(after),'reviewClosure':closure,
                     'reviewClosureSha256':closure_hash,'authoringFile':'data/playtest/spell_drafts/batch_transformations.json',
                     'scope':'Only reviewed operational/status/reviewFlags change; preserved original evidence/access/prices'}
assert len(evolution)==5
write(ROOT/'data/playtest/form_temphp_overlay_evolution.json',{'status':'Exact reviewed five-spell evolution; original capture unchanged','spells':evolution})
profiles=read(ROOT/'data/playtest/spell_form_profiles.json')
profiles['status']='REVIEWED / reference-VALIDATED:12 bounded spell-form profiles'
profiles['reviewClosure']=closure;write(ROOT/'data/playtest/spell_form_profiles.json',profiles)
report=read(ROOT/'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json')
assert report['status']=='PASS' and report['checks']==216
report['reviewStatus']='REVIEWED / reference-VALIDATED: five spell interfaces and12 profiles'
report['reviewClosure']=closure;write(ROOT/'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json',report)
formreport=read(ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json')
formreport['candidateSpellBridge']={'status':'REVIEWED / reference-VALIDATED','change':'Shared spell_anatomies registry + Druid admission guard only','reviewClosure':closure}
write(ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json',formreport)
bindings=read(ROOT/'data/playtest/form_temphp_bindings.json')
bindings['status']='REVIEWED / reference-VALIDATED: selected175+5 roles; five formerly deferred spells now reviewed separately;4 named components remain deferred'
bindings['deferredComponentIds']=[i for i in bindings['deferredComponentIds'] if i not in {'ordinary-spell:'+n for n in IDS}]
assert len(bindings['deferredComponentIds'])==4
for b in bindings['bindings']:
    if b['bindingId'] not in {'ordinary-spell:'+n for n in IDS}:continue
    b.setdefault('historicalClassifications',[])
    if b['classification'] not in b['historicalClassifications']:b['historicalClassifications'].append(b['classification'])
    b['classification']='SPELL — reviewed full ordinary-spell overlay'
    b['status']='REVIEWED / reference-VALIDATED: five-spell completion scope'
    b['reviewEvidence']=list(dict.fromkeys(b['reviewEvidence']+['GPT_TRANSFORMATION_SPELL_FINAL_CLOSURE.md']))
    b['operationalOverrides']=list(dict.fromkeys(b['operationalOverrides']+['Use TRANSFORMATION_SPELL_PLAYTEST.md and exact promoted ordinary-spell overlay;216 checks/729 spatial scenarios.']))
    b['openIssues']=['Wider geometry/item/attack-taxonomy/runtime/balance interfaces remain outside bounded spell closure.']
    b.setdefault('historicalOverlay',deepcopy(b['currentOverlay']))
    b.setdefault('historicalOverlaySha256',b['overlaySha256'])
    b['currentOverlay']=current[b['sourceId']];b['overlaySha256']=digest(current[b['sourceId']])
write(ROOT/'data/playtest/form_temphp_bindings.json',bindings)
guide=ROOT/'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md'
text=guide.read_text(encoding='utf-8').replace('# Transformation and Harmonic Bulwark playtest candidate','# Transformation and Harmonic Bulwark playtest rules',1)
text=text.replace('**Status: discussed draft; implementation review pending.** This guide supplies five ordinary spell overlays and twelve finite forms. It does not yet add them to the operational catalog.',
                  '**REVIEWED / reference-VALIDATED within the five-spell scope.** This guide supplies five promoted operational-playtest overlays and twelve finite forms. The catalog now contains83 operational drafts and765 unfinished spells. The candidate versions remain preserved as review history.')
text=text.replace('`candidate_transformations.json` remains inactive.','`batch_transformations.json` is the reviewed operational source; `candidate_transformations.json` remains inactive historical evidence.')
text=text.replace('Independent review must examine this actual code and its tests before catalog promotion.','GPT independently reviewed the actual code and216 contract checks plus729 spatial scenarios; the [bounded closure](../../../../'+closure+') supports this provisional promotion. Wider interfaces remain open.')
guide.write_text(text,encoding='utf-8')
print('Promoted5 reviewed spells; preserved originals, historical captures and exact reviewed overlay evolution.')
