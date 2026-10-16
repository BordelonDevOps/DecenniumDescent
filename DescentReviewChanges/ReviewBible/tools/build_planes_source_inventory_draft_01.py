"""Inventory plane-related source claims without promoting a cosmological map."""
from datetime import datetime,timezone
from xml.etree import ElementTree as E
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded


def paragraphs(p):
    with zipfile.ZipFile(p) as z:root=E.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    return [''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in root.findall('.//w:p',ns)]


def main():
    candidate=R/'data/director/cosmology/planes_source_inventory_draft_01.json'
    manuscript=R/'docs/director-only/cosmology/PLANES_SOURCE_INVENTORY_DRAFT_01.md'
    receipt=A/'COSMOLOGY_PLANES_SOURCE_INVENTORY_DRAFT_01_CHECK.json'
    assert all(not p.exists() for p in [candidate,manuscript,receipt])
    player=G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx'
    original=G/'The Cosmology of Decennium Descent.docx'
    html=G/'webpage.html';viewer=G/'src/components/CosmologyViewer.tsx';data=G/'src/data/cosmology-lore.json'
    owner=G/'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md'
    paths=[player,original,html,viewer,data,owner,A/'COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json',R/'docs/director-only/cosmology/OWNER_RECONCILIATION_REVIEWED_01.md']
    bindings=[info(p) for p in paths];pp=paragraphs(player);op=paragraphs(original)
    records=[]
    def docx_evidence(path,ps,index):
        return {'path':path.relative_to(G).as_posix(),'part':'word/document.xml','paragraphIndexZeroBased':index,'excerpt':ps[index],'excerptSha256':hashlib.sha256(ps[index].encode()).hexdigest(),'evidenceKind':'exact-source-paragraph'}
    def docrow(name,kind,group,head,detail=None,context=None):
        assert name in pp[head],(name,head,pp[head])
        records.append({'id':f'PC-{len([r for r in records if r["id"].startswith("PC-")])+1:02}', 'label':name,'kind':kind,'group':group,'authority':'mortal cosmographic/religious account in current Appendix B; not objective cosmic proof','evidence':[docx_evidence(player,pp,i) for i in dict.fromkeys([head]+([detail] if detail else [])+([context] if context else []))],'objectiveEquivalenceAdopted':False})
    for name,kind,group,head,detail in [
        ('Material Plane','plane','Material',10115,10117),
        ('Ethereal Plane','plane','Transitive',10131,10133),('Astral Plane','plane','Transitive',10143,10145),('Veiled Expanse','plane','Transitive',10155,10157),('Verdant Reflection','plane','Transitive',10167,10169),
        ('Plane of Earth','plane','Elemental',10187,None),('Plane of Water','plane','Elemental',10188,None),('Plane of Air','plane','Elemental',10189,None),('Plane of Fire','plane','Elemental',10190,None),
        ('Plane of Ice','plane','Para-elemental',10193,None),('Plane of Magma','plane','Para-elemental',10194,None),('Plane of Ooze','plane','Para-elemental',10195,None),('Plane of Smoke','plane','Para-elemental',10196,None),
        ('Plane of Positive Energy','plane','Energy',10204,None),('Plane of Negative Energy','plane','Energy',10205,None),('Plane of Arcane Energy','plane','Energy',10206,None),('Plane of Psionic Energy','plane','Energy',10207,None),
        ('Fields of Grace','plane','Upper',10219,None),('Sevenfold Ascent','plane','Upper',10220,None),('Wildbloom Courts','plane','Upper',10221,None),('Ordered Marches','plane','Upper',10222,None),('Twin Hearths','plane','Upper',10223,None),
        ('Nine Infernal Courts','plane','Lower',10231,None),('Abyss','plane','Lower',10232,None),('Red Prison','plane','Lower',10233,None),('Ashen Waste','plane','Lower',10234,None),('Cinder Slopes','plane','Lower',10235,None),
        ('Clockwork Mandala','plane','Neutral',10243,None),('Chaos Sea','plane','Neutral',10244,None),('Concordant Expanse','plane','Neutral',10245,None),("Hero's Reach",'plane','Neutral',10246,None),('War-Cube Marches','plane','Neutral',10247,None),
    ]:docrow(name,kind,group,head,detail)
    for group,kind,context,items in [
        ('Elemental Courts','court',10331,[('Earthen Conclave',10334),('Abyssal Tides',10335),('Tempest Dominion',10336),('Eternal Flame',10337)]),
        ('Fey Courts','court',10343,[('Summer Court',10346),('Winter Court',10347),('Twilight Court',10348),('Dawn Court',10349)]),
        ('Shadow Conclave','conclave member',10355,[('Raven Regent',10358),('Nightlord',10359),('Grief Sovereign',10360),('Forgotten King',10361)]),
        ('Astral Dominions','dominion/site',10367,[('Silver Citadel',10370),('Dream Bazaar',10371),('Thought Forge',10372),('Void Archives',10373)]),
    ]:
        for name,i in items:docrow(name,kind,group,i,context=context)
    for name,i in [('Sigil Compact',10381),('Order of the Gatekeepers',10385),("Planar Cartographers' Guild",10389),('Illuminated Path',10393)]:docrow(name,'faction','Planar Factions',i,i+2,10379)
    for name,i in [('Elemental Convergence',10401),('Shadow Ascendancy',10405),('Fey Schism',10409),('Infernal Conspiracy',10413)]:
        docrow(name,'campaign tension','Current Planar Tensions',i,i+2,10399)
        records[-1]['campaignEpochAdopted']=False
    assert len(records)==56 and sum(r['kind']=='plane' for r in records)==32
    for n,(name,kind,indices) in enumerate([
        ('Bastion of Flame','primary realm',[63,64]),('Veiled Expanse','primary realm',[64,65]),('Radiant Currents','primary realm',[65,66]),('Boundless Void','primary realm',[67,68]),
        ('Molten Glass Tapestries','tributary realm',[71]),('Luminous Dusk','tributary realm',[71]),('Whispering Archive','tributary realm',[71]),('Calculated Pyre','tributary realm',[71]),
    ],1):
        assert any(name in op[i] for i in indices)
        records.append({'id':f'OR-{n:02}','label':name,'kind':kind,'group':'Original Planes Ascendant','authority':'original cosmology manuscript; chronology and identity claims qualified by later owner decisions','evidence':[docx_evidence(original,op,i) for i in indices],'objectiveEquivalenceAdopted':False})
    html_lines=html.read_text(encoding='utf-8').splitlines();view_lines=viewer.read_text(encoding='utf-8').splitlines()
    def line_ev(p,lines,i):return {'path':p.relative_to(G).as_posix(),'lineOneBased':i+1,'excerpt':lines[i],'evidenceKind':'exact-source-line'}
    for n,(name,needle,kind) in enumerate([
        ("Calan'thir – Axis of the Celestial Spiral",'calanthirCore.userData.name =','diagram axis label'),
        ('Infernal Spiral',"label: 'Infernal Spiral'",'diagram shell label'),('Elemental Ring',"label: 'Elemental Ring'",'diagram shell label'),('Primordial Mandala',"label: 'Primordial Mandala'",'diagram shell label'),('Celestial Arc',"label: 'Celestial Arc'",'diagram shell label'),
    ],1):
        indices=[i for i,s in enumerate(html_lines) if needle in s];assert len(indices)==1
        evidence=[line_ev(html,html_lines,indices[0])]
        if n==1:evidence.extend(line_ev(html,html_lines,i) for i,s in enumerate(html_lines) if 'calanthirCore.userData.description' in s)
        records.append({'id':f'WH-{n:02}','label':name,'kind':kind,'group':'Saved standalone website','authority':'saved visualization source; objective geometry, hierarchy and mapping are not independently approved by its layout','evidence':evidence,'objectiveEquivalenceAdopted':False})
    lore=json.loads(data.read_bytes())
    for n,row in enumerate(lore['planes']):
        indices=[i for i,s in enumerate(view_lines) if 'name: "'+row['name']+'"' in s];assert len(indices)==1
        records.append({'id':f'WV-{n+1:02}','label':row['name'],'kind':'viewer body/selector label','group':'Companion website','authority':'companion presentation claim; preserve summary without promoting display coordinates into cosmological measurements','sourceSummary':row['summary'],'evidence':[{'path':data.relative_to(G).as_posix(),'jsonPointer':f'/planes/{n}','value':row,'evidenceKind':'exact-json-value'},line_ev(viewer,view_lines,indices[0])],'objectiveEquivalenceAdopted':False})
    assert len(records)==76 and len({r['id'] for r in records})==76
    contexts=[docx_evidence(player,pp,i) for i in [9977,10111,10113,10125,10135,10145,10147,10198,10209,10213,10253,10257,10258,10259,10260,10261,10263,10267,10268,10269,10270,10271,10273,10277,10278,10279,10280,10281,10283,10289,10319,10327,10339,10351,10363,10375]]
    dependencies=[
        {'id':'PLD-01','issue':'Map equivalences','status':'Review pending','detail':'Four original primaries, four original tributaries,32 mortal plane labels,4 standalone shell labels plus its axis, and 7 companion bodies are source-claim groups, not a single 76-plane ontology.'},
        {'id':'PLD-02','issue':'Rulers and soul jurisdiction','status':'Review pending','detail':'Four elemental courts and four Fey courts name ruler titles. Four Shadow Conclave members claim domains including death/memory; four Astral dominions are sites, not four rulers. Do not flatten these into sixteen equivalent gods.'},
        {'id':'PLD-03','issue':'Named factions and publication terminology','status':'Review pending','detail':'Four planar factions are now explicitly indexed. Sigil/Far Realm references remain preserved source text and already-known publication review dependencies, not silent replacement targets.'},
        {'id':'PLD-04','issue':'Campaign epoch and hooks','status':'Review pending','detail':'Four current tensions in Appendix B do not establish that the original saga epilogue or every tension is active in the current Opening. Void Sovereign is a named entity claim within Shadow Ascendancy, not an automatic identity for Boundless Void, Old God or survivor.'},
        {'id':'PLD-05','issue':'Travel/time mechanics','status':'Review pending','detail':'Connections, time descriptions, portals and services must be read with exact reviewed effects and expedition boundaries. No durations, clocks, rest rewards, costs, consent rules, or planar spell procedure is created here.'},
        {'id':'PLD-06','issue':'Owner clarification and Q6','status':'Partially pending','detail':'Pending Heartcell-builder clarification and Q6 conference remain separate. Recorded crystal path/public ceiling exists; identity/stat gaps remain. This inventory neither reopens settled scope nor supplies missing identity.'},
    ]
    result={'reviewId':'COSMOLOGY-PLANES-SOURCE-INVENTORY-DRAFT-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'source inventory draft; actual GPT planes review pending','visibility':'director-only','publicExport':False,'sourceBindings':bindings,'recordCount':76,'counts':{'mortalPlaneLabels':32,'courtMemberAndDominionEntries':16,'planarFactions':4,'campaignTensions':4,'originalRealms':8,'standaloneWebsiteLabels':5,'companionWebsiteBodies':7},'records':records,'contextEvidence':contexts,'dependencies':dependencies,'semanticReadThisPass':'Player P10111–10415 in sequence, plus P10417–10474 as next-history boundary; saved HTML and viewer/source data previously read. Original P60–76 and court/plane passages already read in prior local concordance. Only exact cited excerpts are reproduced in this index.','newLoreAdopted':False,'newRulesAdopted':False,'sourceInformationDeleted':0,'fullCosmologyApproved':False}
    candidate.write_bytes(encoded(result))
    text=['# Planes and courts — source inventory for joint review','', '**Status: draft source index.** This records 76 source claims, not 76 distinct planes. It does not merge maps, choose new canon, authorize travel, or make a public handout. Read the current owner-correction companion and registered Q6 decisions alongside these sources.','', 'The saved standalone visualization and the companion website are included explicitly. Their diagram labels are retained as presentation evidence. The companion’s twelve First Song chapter bodies match original manuscript passages after whitespace normalization; its World I–VI entry still contains a gap.','']
    for group in dict.fromkeys(r['group'] for r in records):
        text+=['## '+group,'','| Record | Label | Kind | Source |','|---|---|---|---|']
        for r in records:
            if r['group']!=group:continue
            e=r['evidence'][0];locator='P'+str(e['paragraphIndexZeroBased']) if 'paragraphIndexZeroBased' in e else ('line '+str(e['lineOneBased']) if 'lineOneBased' in e else e['jsonPointer'])
            text.append('| '+r['id']+' | '+r['label'].replace('|','\\|')+' | '+r['kind']+' | '+e['path']+' — '+locator+' |')
        text.append('')
    text+=['## What remains to decide','']
    for d in dependencies:text.append('- **'+d['issue']+':** '+d['detail'])
    text+=['','Exact paragraph excerpts, line references, JSON values and source hashes are retained in [the structured source inventory](../../../data/director/cosmology/planes_source_inventory_draft_01.json). Paragraph numbers are zero-based positions of every Word paragraph, including blank paragraphs and table cells.','', 'No original source, website file or earlier receipt was changed. GPT review, runtime verification, human playtesting and publication approval remain outstanding.','']
    manuscript.write_text('\n'.join(text),encoding='utf-8',newline='\n')
    assert all(info(G/x['path'])==x for x in bindings)
    receipt.write_bytes(encoded({'reviewId':result['reviewId'],'recordedAtUtc':result['recordedAtUtc'],'candidate':info(candidate),'manuscript':info(manuscript),'counts':result['counts'],'recordCount':76,'allSourceHashesUnchanged':True,'exactCitationConstruction':'Every named DOCX label asserted present at its stated paragraph; excerpts copied directly from source XML. Website line needles unique; JSON values copied exactly.','sourceInformationDeleted':0,'newLoreAdopted':False,'newRulesAdopted':False,'gptPlanesReviewCompleted':False}))
    print(json.dumps({'candidate':info(candidate),'manuscript':info(manuscript),'check':info(receipt),'records':76,'sourceFiles':len(bindings),'sourceInformationDeleted':0}))


if __name__=='__main__':main()
