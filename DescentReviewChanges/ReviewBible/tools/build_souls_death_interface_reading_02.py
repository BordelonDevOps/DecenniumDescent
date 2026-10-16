"""Capture further source reading for souls, Research, and similarly named spells."""
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json,re
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    target=A/'COSMOLOGY_SOULS_DEATH_INTERFACE_READING_02.json'
    receipt=A/'COSMOLOGY_SOULS_DEATH_INTERFACE_READING_02_CHECK.json'
    assert not target.exists() and not receipt.exists()
    bindings={};passages=[];objects=[]
    def bind(p):
        row=info(p);bindings[row['path']]=row;return row['path']
    n={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for p,indices in [
        (G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx',[9977]+list(range(10350,10365))),
        (G/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',list(range(1276,1309))),
        (G/'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx',list(range(893,899))+list(range(1434,1439))),
    ]:
        path=bind(p)
        with ZipFile(p) as z:root=E.fromstring(z.read('word/document.xml'))
        a=[''.join(t.text or '' for t in el.findall('.//w:t',n)) for el in root.findall('.//w:p',n)]
        for i in indices:passages.append({'path':path,'part':'word/document.xml','paragraphIndexZeroBased':i,'text':a[i],'textSha256':hashlib.sha256(a[i].encode()).hexdigest()})
    p=R/'data/public/spell_playtests/catalog.json';path=bind(p);cat=read(p)
    for i in [207,292,370,393,628,635,667,824]:
        objects.append({'path':path,'jsonPointer':f'/spells/{i}','kind':'complete-current-spell-card','value':cat['spells'][i]})
    assert sum(x['value']['operational'] is not None for x in objects)==1
    p=R/'data/director/higher_spell_operating_proposal_index.json';path=bind(p)
    for i,x in enumerate(read(p)['entries']):
        if x['spellId'] in {'soul-reflection','soul-cage','erase-soul','clone','arcane-clone'}:
            objects.append({'path':path,'jsonPointer':f'/entries/{i}','kind':'proposal-status-only','value':x})
    p=R/'data/director/spell_proposals/transmutation_universal_rank6.json';path=bind(p);draft=read(p)['records'][8]
    assert draft['spellId']=='arcane-clone' and draft['status']=='unadopted-unsent-operating-proposal'
    objects.append({'path':path,'jsonPointer':'/records/8','kind':'complete-unadopted-Arcane-Clone-proposal','value':draft})
    discovery=[{'jsonPointer':f'/spells/{i}','id':s['id'],'status':s['status'],'hasOperationalProcedure':s['operational'] is not None}
               for i,s in enumerate(cat['spells']) if re.search(r'soul|death|resurrect|reincarn|clone|reviv|infernal pact',s['name'],re.I)]
    findings=[
        {'id':'SD2-01','finding':'The Player appendix explicitly frames its theology/plane diagram as mortal belief (P9977). Its Shadow Conclave claims death/fate/darkness/memory domains and agents collecting souls (P10355–10363). These are not objective proof of a universal afterlife jurisdiction or identity with the original Choir/Argent Gate.'},
        {'id':'SD2-02','finding':'Core P1302 already requires the Matrix primary researcher personally to possess high ranks in Arcana, History, Religion, Nature and Engineering, cross-referencing rare drops, libraries, mechanisms and seasonal changes. Archive knowledge may be inherited; cognitive continuity usually cannot. The text supplies no numeric definition of high ranks or complete research progression. Ordinary spell research is Arcana plus laboratory. Do not replace this with one generic roll or silently decide what the owner meant by Research skill.'},
        {'id':'SD2-03','finding':'The ritual scale table includes Grand resurrection and Seasonal Matrical theorem examples; table scale is not a complete operational permission or Hunt intervention. Director P896 supplies translation/identification/mapping roles; P1435/1437 recommends distributed Gate clues and avoiding single-roll campaign gates. These can inform design, not prove the Equation has four fragments or a fixed solution.'},
        {'id':'SD2-04','finding':'Soul Mark is reviewed and tracks a continuing nondead creature with its actual endpoint/same-plane bearing rules. It ends on death/destruction and does not track a detached soul, corpse or later replacement body. The name does not authorize an afterlife beacon.'},
        {'id':'SD2-05','finding':'Erase Soul is pending and its original effect is three-round identity confusion/inability to act with WIS early negation, not permanent metaphysical annihilation. Soul Mirror is pending one-spell reflection. Soul Reflection is pending a three-round self-combat version. Their names cannot settle cessation metaphysics.'},
        {'id':'SD2-06','finding':'Clone has only a source question, no completed procedure or joint review. Its biological death-insurance description makes it a future Hunt interface, not an already available escape. Arcane Clone instead preserves an illusionary caster copy for three rounds; the full TU6-09 draft is unadopted and explicitly denies biological clone, death replacement or soul transfer.'},
        {'id':'SD2-07','finding':'Ordinary Soul Cage remains a literal post-push receipt without an adopted procedure. Its Enchantment/ Necromancy variants differ between a dying creature and dying humanoid. A similarly named shield in another source does not approve this ordinary spell. Soulburn Pact is pending HP/RP exchange with preserved3versus5RP source conflict; it is not a soul-contract or divine intervention grant.'},
    ]
    record={'reviewId':'COSMOLOGY-SOULS-DEATH-INTERFACE-READING-02','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
            'status':'Bounded local semantic reading, unsubmitted; no new rules adopted','previousReading':info(A/'COSMOLOGY_SOULS_DEATH_SOURCE_READING_01.json'),
            'sourceBindings':list(bindings.values()),'docxPassages':passages,'objects':objects,'nameDiscoveryOnly':discovery,'findings':findings,
            'coverage':{'completeDocxParagraphs':60,'completeCurrentSpellCards':8,'reviewedAmongThoseCards':1,'pendingAmongThoseCards':7,'completeUnadoptedProposals':1,'proposalStatusEntries':5,
                        'notClaimed':'The name-based discovery list is not semantic review of its other matches. No full book, whole catalog, whole research system or universal afterlife claim.'},
            'remainingSourceWork':['Actual infernal legal/contract/body-claim procedures beyond lore references','Relevant remaining soul-blocking and revival sources, using individual complete procedures','Current temporal parent/control interfaces if proposing their concrete operation'],
            'newMechanicsAdopted':False,'sourceInformationDeleted':0,'spellFlagsChanged':False,'fullCosmologyApproved':False}
    assert len(passages)==60 and len(objects)==14 and len(bindings)==6
    target.write_bytes(encoded(record))
    for row in bindings.values():assert info(G/row['path'])==row
    receipt.write_bytes(encoded({'record':info(target),'sourceBindingsVerified':6,'paragraphs':60,'completeCurrentSpellCards':8,'pendingStillPending':7,'completeUnadoptedProposal':1,'discoveryOnlyNames':len(discovery),'newMechanicsAdopted':False}))
    print(json.dumps(read(receipt)))

if __name__=='__main__':main()
