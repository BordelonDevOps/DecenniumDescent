"""Apply only the completed AEX-01–07 editorial verdict, preserving submitted bytes.

This authors corrected rules; it does not promote recipes or implement a runtime.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json
import re
import shutil
from build_advanced_craft_internal_candidates import read, dump, sha, render_card, val
from build_advanced_craft_public_candidates import build_projection, body_markdown, GUIDE, BODY

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
V = A/'advanced167-exact-reviewer-files'
REPLY = 'd35f30fb-dbf5-4cc6-a8ba-2d4698c0be91'
VERDICT_HASH = '87db8f8b373d497444bbd3b6b43e4dfd0b4eedf4f4239312af7bf513ace3f250'
TRADES = ['Enchanting', 'Rune Carving', 'Scribing', 'Tinkering']


def correction_quotes():
    """Read exact published replacement paragraphs as data, never executable code."""
    reg = read(V/'AEX_167_CORRECTIONS.json')
    assert reg['verdictSha256'] == sha(V/reg['verdictFile']) == VERDICT_HASH
    out = {}
    for c in reg['corrections']:
        out[c['id']] = re.findall(r'^> (.+)$', c['completeCorrectionSpecificationMarkdown'], re.M)
    assert {k:len(v) for k,v in out.items()} == {'AEX-01':1,'AEX-02':4,'AEX-03':1,'AEX-04':1,'AEX-05':1,'AEX-06':1,'AEX-07':1}
    return out


Q = correction_quotes()
RECOVERY = Q['AEX-01'][0]
GROUND, INSPECT, BINDING, TRAP = Q['AEX-02']
SERVICE = Q['AEX-03'][0]
DISABLE = Q['AEX-04'][0]
MODEL = Q['AEX-05'][0]
WARD = Q['AEX-06'][0]
CONSULT = Q['AEX-07'][0]
EQUATION = 'recovered_i = u_i × floor(min(Q_i / 4, R_i) / u_i)'
EQUATION_TEXT = ('For each exact eligible identity in this batch, use `'+EQUATION+'`. '
                  'Q_i is its fixed consumed-input quantity; R_i is the eligible amount surviving from those same inputs; u_i is its legal source-unit precision. '
                  'Group only genuinely identical eligible inputs within this same batch while retaining every physical occurrence. Catalysts and unrelated batches do not enter that recovery group.')


def replace_once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new, 1)


def main():
    backup = A/'advanced167-before-aex-corrections'
    assert not backup.exists(), 'One-use application: inspect existing correction receipt instead of rerunning.'
    ip = R/'data/director/advanced_craft_recipe_candidate_internal.json'
    pp = R/'data/crafting/advanced_craft_recipe_candidate_public.json'
    d = read(ip); prior_public = read(pp)
    receipt = read(A/'ADVANCED_CRAFT_EXACT_SUBMISSION.json')
    capture = read(A/'ADVANCED_CRAFT_EXACT_VERDICT_CONNECTOR_CAPTURE.json')
    assert any(i.get('id') == REPLY for t in capture['turns'] for i in t['items'])
    assert sha(A/'DD_Advanced_Craft_167_Exact_Review_v1.zip') == 'a29420353145c4c91ebb472f2843a3ea14041b38eb49b93420ec99294c03b1a7'
    protected = read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes']
    assert all(sha(G/p) == h for p,h in protected.items())
    files = [ip,pp,R/d['sharedGuide'],R/d['bodyGuide'],R/GUIDE,R/BODY]
    files += [R/f'docs/{aud}/{t.upper().replace(" ","_")}_{suffix}.md' for aud,suffix in [('director-only','INTERNAL_RECIPE_CARDS'),('mechanics','CANDIDATE_RECIPE_CARDS')] for t in TRADES]
    files += [A/n for n in ['ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json','ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json','ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json','ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json','ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json','ADVANCED_CRAFT_WORKED_CASE_VALIDATION.json','ADVANCED_CRAFT_INTERNAL_MANUFACTURING_OUTCOMES.json','ADVANCED_CRAFT_AUTHORING_PROGRESS.json','ADVANCED_CRAFT_CANDIDATE_READINESS.json']]
    files += [R/'tools'/n for n in ['validate_advanced_craft_internal_candidates.py','validate_advanced_craft_public_candidates.py','validate_advanced_craft_worked_cases.py']]
    old=[]
    for p in files:
        dest=backup/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        old.append({'path':p.relative_to(G).as_posix(),'sha256':sha(p)})
    dump(backup/'MANIFEST.json',old)
    appmap={f'AEX-{i:02}':[] for i in range(1,8)}
    amendments={
        'AC-04':[('AEX-01',RECOVERY+'\n\n'+EQUATION_TEXT)],
        'RC-01':[('AEX-02',GROUND)],'RC-02':[('AEX-02',INSPECT)],'RC-04':[('AEX-02',BINDING)],
        'TI-02':[('AEX-02',TRAP)],'TI-05':[('AEX-03',SERVICE)],'TD-08':[('AEX-04',DISABLE)],
        'B-04':[('AEX-05',MODEL)],'RC-07':[('AEX-06',WARD)],'SC-05':[('AEX-07',CONSULT)]}
    for sid,changes in amendments.items():
        s=d['procedureSections'][sid]
        s['controllingText']=s.get('controllingText',s['text'])+'\n\n'+'\n\n'.join('**'+cid+' — controlling clarification:** '+txt for cid,txt in changes)
        s['exactReviewAmendments']=[cid for cid,_ in changes]
    body=d['bodyModels']['TI-device'];body['operationalModelDescription']=MODEL
    body.setdefault('controllingCorrections',[]).append('AEX-05')
    for bid,b in d['bodyModels'].items():
        if bid.startswith('TI-'):b['operationalBodyText']=d['procedureSections']['B-04']['controllingText']
    for c in d['cards']:
        o=c['operational']; profile=o['profile']; paragraphs={p['label']:p for p in o['paragraphs']}
        applied=['AEX-01']
        p=paragraphs['Retention and failure']
        p['text']=replace_once(p['text'],'Failed creation recovers 25% of genuinely remaining consumed non-catalyst quantities by exact identity and legal unit precision, capped by actual remains.',RECOVERY+' '+EQUATION_TEXT)
        effect=paragraphs['Effect and operation']
        if c['sourceRecipe']['skill']=='Rune Carving' and c['recipeId']!='recipe-667':
            o['paragraphs'].insert(1,{'label':'Rune control and examination','text':GROUND+'\n\n'+INSPECT})
            applied.append('AEX-02')
        if profile=='RC-binding':
            effect['text']=replace_once(effect['text'],'Leaving the original square or moving/suppressing the original plate ends this restraint.',BINDING)
            effect['text']=replace_once(effect['text'],'RC-02–04','RC-01–04');applied.append('AEX-07')
        elif profile=='RC-explosive':
            effect['text']=replace_once(effect['text'],'RC-02/03/05','RC-01–03 and RC-05');applied.append('AEX-07')
        elif profile=='RC-healing':
            effect['text']=replace_once(effect['text'],'RC-02/03/06','RC-01–03 and RC-06');applied.append('AEX-07')
        elif profile=='RC-warding':
            o['useBinding']['trigger']=WARD
            effect['text']=replace_once(effect['text'],'Outside initiative use the RC-07 six-second marker.','Outside initiative use the RC-08 six-second marker.')
            applied.extend(['AEX-06','AEX-07'])
        elif profile=='SC-script':
            effect['text']=replace_once(effect['text'],'The +research requires actual relevant consultation under SC-04, and never improves creating this bonus item. SC-01–04 and SC-10 govern the full procedure.','The research bonus requires the actual relevant lead consultation under SC-05. SC-01–05 and SC-10 govern the full procedure. '+CONSULT)
            applied.append('AEX-07')
        elif profile=='SC-reference':
            effect['text']=replace_once(effect['text'],'SC-04/07/08/10 provide the full boundaries.','SC-04, SC-05, SC-07, SC-08 and SC-10 provide the applicable full boundaries. '+CONSULT)
            applied.append('AEX-07')
        elif profile=='TI-trap':
            effect['text']=replace_once(effect['text'],'TI-02 gives full disarm rules.',TRAP+' TI-02 gives the remaining full disarm rules.')
            applied.append('AEX-02')
        elif profile=='TI-automaton':
            o['useBinding']['serviceUnit']=SERVICE
            effect['text']=replace_once(effect['text'],'one genuine encounter for at most ten elapsed minutes, or one ten-minute noncombat operating block, paid at block start.',SERVICE+' Outside encounters, first actual operation spends one service unit for one ten-elapsed-minute noncombat block.')
            applied.append('AEX-03')
        if c['sourceRecipe']['skill']=='Tinkering':
            o['paragraphs'].insert(1,{'label':'Routed Dissonance','text':'Only the acquired TD-08 feature, once per genuine short rest, permits a Bonus Action to route up to two current Dissonance into one own active qualifying device within 30 feet. '+DISABLE+' An invalid blocked declaration spends nothing; a later disable does not refund a previously legal committed cost. Actual Field Repair, the existing ten-active-minute/1RP/Tinker\'s-tools procedure, the origin Tinker\'s next completed genuine short rest or completed qualifying ordinary repair may clear only the permitted functional state. A buyer\'s unrelated rest does not clear it.'})
            applied.append('AEX-04')
        if 'TI-device' in o['bodyModelIds']:
            paragraphs['Complete output bodies']['text']=replace_once(paragraphs['Complete output bodies']['text'],body['sourceAuthoringProfile']['model'],MODEL)
            applied.append('AEX-05')
        o['exactReviewCorrections']=sorted(set(applied))
        for cid in o['exactReviewCorrections']:appmap[cid].append(c['recipeId'])
        c['manuscriptText']=render_card(c)
    for cid,ids in appmap.items():assert ids,cid
    expected={x['id']:set(x['affectedRecipeIds']) for x in read(V/'AEX_167_CORRECTIONS.json')['corrections']}
    assert all(set(ids)==expected[cid] for cid,ids in appmap.items()), {k:len(v) for k,v in appmap.items()}
    for i in range(1,8):
        cid=f'AEX-{i:02}'
        d['controllingCorrections'].append({'id':cid,'replyId':REPLY,'verdictFile':(V/'AEX_167_Exact_Review_Verdict.md').relative_to(G).as_posix(),'verdictSha256':VERDICT_HASH,'affectedRecipeIds':appmap[cid],'status':'applied; finite checks and promotion receipt pending'})
    d['status']='exact-review-corrections-applied-validation-pending'
    dump(ip,d)
    gp=(R/GUIDE).read_text(encoding='utf-8')
    gp=replace_once(gp,'Failed creation returns 25% of each exact consumed non-catalyst identity, capped by actual remaining material and rounded down to its legal source unit.',RECOVERY+' '+EQUATION_TEXT)
    gp=replace_once(gp,'Moving it disarms it; covering, suppression, incompleteness or Broken structure prevents a new valid trigger.',GROUND)
    oldinspect=next(x for x in gp.split('\n\n') if x.startswith('Inspecting an accessible rune'))
    gp=replace_once(gp,oldinspect,INSPECT)
    gp=replace_once(gp,'Leaving the bound square or moving/suppressing the original plate ends that particular restraint.',BINDING)
    gp=replace_once(gp,'An unfamiliar disarm requires',TRAP+' An unfamiliar disarm requires')
    gp=replace_once(gp,'Spend one when a genuine encounter starts, covering at most ten elapsed minutes; continuing longer needs another. A distinct encounter needs another even if the last one was short.',SERVICE)
    gp=replace_once(gp,'The routed disabled state stops applicable movement, attacks and device aura functions; it refills no RP/Refrain or charges, and clocks continue.',DISABLE)
    gp=replace_once(gp,'A script does not improve creating itself.',CONSULT)
    gp=replace_once(gp,'Extra turns do not advance regular-turn expiry or supply another Reaction.',
        'Extra turns do not advance regular-turn expiry or supply another Reaction. Removing the plate, melding, Broken or incomplete state, suppression or other lost eligibility suspends the remaining ward benefit while its original deadline runs. If eligibility returns before that deadline, only the still-unexpired original benefit can resume; there is no new activation, refunded charge or extended duration. This is distinct from an ended Binding restraint and an invalidated ground trigger.')
    # All public locators resolve to public procedural headings; no private profile is exported.
    legend=[('AC-01','Make one recorded work order'),('AC-02–03','Resolve the six creation outcomes'),('AC-04','Inputs, retained tools and failure returns'),('AC-05','Training, access and work'),('AC-06–07','Structure, state and repair'),('AC-08–10','Structure, state and repair'),('EN-01–10','Enchanting'),('RC-01–09','Rune Carving'),('SC-01–05','Scribing'),('SC-06–07','Scribing'),('SC-08','Scribing — Language Insight'),('SC-10','Scribing'),('TI-01–07','Tinkering'),('TI-10','Tinkering'),('TD-01–18','Tinker class interfaces'),('B-01–05','Body catalogue')]
    anchors={'Make one recorded work order':'make-one-recorded-work-order','Resolve the six creation outcomes':'resolve-the-six-creation-outcomes','Inputs, retained tools and failure returns':'inputs-retained-tools-and-failure-returns','Training, access and work':'training-access-and-work','Structure, state and repair':'structure-state-and-repair','Enchanting':'enchanting','Rune Carving':'rune-carving','Scribing':'scribing','Scribing — Language Insight':'scribing','Tinkering':'tinkering','Tinker class interfaces':'tinker-class-interfaces'}
    gp+='\n\n## Public procedure locator\n\nThese section IDs on a card locate the applicable ordinary procedure below. Read the complete linked procedure and the actual card together. Only the relevant public scope is supplied; section IDs do not grant access to a different item or hidden dossier.\n\n| Card locator | Public procedure |\n|---|---|\n'
    for code,title in legend:
        link='ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md' if title=='Body catalogue' else '#'+anchors[title]
        gp+=f'| {code} | [{title}]({link}) |\n'
    gp+='\nSC-08 here means only the Language Insight earning, evidence, cap and literal-passage study procedure under Scribing. The research/navigation exclusions in that same section apply to the complete item, its authoring, copying, encoding and derivative production.\n'
    (R/GUIDE).write_text(gp,encoding='utf-8')
    # Regenerate active internal procedures from original plus identified amendments.
    sec=d['procedureSections']
    (R/d['sharedGuide']).write_text('# Advanced crafting — internal operating guide\n\n**Exact corrections AEX-01–07 applied; validation and promotion receipt pending.** ADV-EDIT-01 remains controlling. Original section text is preserved in the internal JSON and immutable review evidence; the active sections below include the named amendments.\n\n'+'\n\n'.join(f"## {s['id']} — {s['title']}\n\n{s.get('controllingText',s['text'])}" for s in sec.values())+'\n',encoding='utf-8')
    lines=['# Advanced crafting — internal body catalogue','','**Exact corrections applied; validation pending.** Active model descriptions below control their preserved historical source profiles. The complete original profiles remain unchanged in the internal JSON and submitted archive.','']
    for bid,b in d['bodyModels'].items():
        active=deepcopy(b['sourceAuthoringProfile']);active['model']=b.get('operationalModelDescription',active['model']);active['primary']=b.get('operationalPrimaryRule',active['primary'])
        lines.extend(['## '+bid,'',json.dumps(active,ensure_ascii=False,indent=2),''])
    lines += [f"## {sid} — {sec[sid]['title']}\n\n{sec[sid].get('controllingText',sec[sid]['text'])}" for sid in ['B-01','B-02','B-03','B-04','B-05']]
    lines+=['## Existing alternate hosts','','Each listed existing source template still requires complete actual physical registration. No unsupported special model, ammunition bundle, shield, natural attack, no-damage net or already magical host.','']
    lines += [f"- {x['sourceEquipmentRecord']['name']} ({key}): {val(x['ordinaryPriceGp'])} gp; {x['ordinaryWeightLb']} lb; ordinary B{x['baselineStructuralHP']}; {json.dumps(x['sourceEquipmentRecord']['sourceFields'],ensure_ascii=False)}" for key,x in d['enchantingHostModels'].items()]
    (R/d['bodyGuide']).write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
    cards,bodies,hosts,ledger=build_projection(d,read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'))
    bodies['TI-device']['bodyText']=MODEL+' '+bodies['TI-device']['bodyText']
    btext=body_markdown(bodies,hosts);(R/BODY).write_text(btext,encoding='utf-8')
    public=deepcopy(prior_public);public.update(cards=cards,bodyModels=bodies,enchantingHostModels=hosts,operatingGuideText=gp,bodyGuideText=btext,status=d['status'])
    dump(pp,public)
    for trade in TRADES:
        for audience,suffix,cs in [('director-only','INTERNAL_RECIPE_CARDS',d['cards']),('mechanics','CANDIDATE_RECIPE_CARDS',cards)]:
            selected=[c for c in cs if c['sourceRecipe']['skill']==trade]
            p=R/f'docs/{audience}/{trade.upper().replace(" ","_")}_{suffix}.md'
            p.write_text(f'# {trade} — recipe candidates\n\n**{len(selected)} cards; exact corrections applied, validation and promotion receipt pending.** Sources and original book prose remain preserved.\n\n'+'\n'.join(c['manuscriptText'] for c in selected),encoding='utf-8')
    projection=read(A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json');projection.update(entries=ledger,internalCandidateSha256=sha(ip),status='Exact corrections applied; full-envelope validation pending');dump(A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json',projection)
    assert all(sha(G/p)==h for p,h in protected.items())
    application={'status':'AEX-01–07 applied; promotion not yet granted','appliedAtUtc':datetime.now(timezone.utc).isoformat(),'replyId':REPLY,'verdictSha256':VERDICT_HASH,'applicationMap':appmap,'publicLocatorLegend':legend,'backup':backup.relative_to(G).as_posix(),'preservedPriorFiles':len(old),'protectedSourceHashes':protected,'protectedSourcesUnchanged':138,'internalCandidateSha256':sha(ip),'publicCandidateSha256':sha(pp),'newApprovals':0}
    dump(A/'ADVANCED_CRAFT_AEX_APPLICATION.json',application)
    print(json.dumps({k:v for k,v in application.items() if k not in ['applicationMap','protectedSourceHashes','publicLocatorLegend']},indent=2))


if __name__=='__main__':main()
