"""Read-only source extraction for the taint/Hunt conference; no rule adoption."""
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    target=A/'COSMOLOGY_TAINT_RESEARCH_SOURCE_READING_04.json'
    check=A/'COSMOLOGY_TAINT_RESEARCH_SOURCE_READING_04_CHECK.json'
    assert not target.exists() and not check.exists()
    bindings={};paras=[];objects=[];sections=[]
    def bind(p):
        row=info(p);bindings[row['path']]=row;return row['path']
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for p,indices in [(G/'The Decennium Descent and the Matrix of Oblivion.docx',list(range(273,290))),
                      (G/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',[489,506,737,738,777,778,1274,1275])]:
        path=bind(p)
        with ZipFile(p) as z:root=E.fromstring(z.read('word/document.xml'))
        a=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in root.findall('.//w:p',ns)]
        for i in indices:paras.append({'path':path,'part':'word/document.xml','paragraphIndexZeroBased':i,'text':a[i],'textSha256':hashlib.sha256(a[i].encode()).hexdigest()})
    for p,ranges in [(R/'docs/canon/UNITY_FALSE_RESONANCE.md',None),
                     (G/'docs/manuals/Instruments_of_the_Weave.md',[(342,383)]),
                     (G/'docs/manuals/Codex_of_the_Heartcell.md',[(81,81),(111,111)])]:
        path=bind(p);lines=p.read_text(encoding='utf-8').splitlines()
        for lo,hi in ranges or [(1,len(lines))]:
            assert hi<=len(lines);text='\n'.join(lines[lo-1:hi])
            sections.append({'path':path,'firstLineOneBased':lo,'lastLineOneBased':hi,'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()})
    p=R/'data/public/spell_playtests/catalog.json';path=bind(p);d=read(p)
    for i in [11,29,36,67,75,94,130,214,230]:objects.append({'path':path,'jsonPointer':f'/spells/{i}','kind':'complete-current-spell-card','value':d['spells'][i]})
    assert sum(x['value']['operational'] is not None for x in objects)==6
    p=R/'data/director/higher_spell_operating_proposal_index.json';path=bind(p);d=read(p)
    for i in [168,218,347]:objects.append({'path':path,'jsonPointer':f'/entries/{i}','kind':'proposal-status-only','value':d['entries'][i]})
    p=R/'data/director/spell_proposals/abjuration_conjuration_rank6.json';path=bind(p);v=read(p)['records'][4]
    assert v['spellId']=='corruption-purge' and v['status']=='unadopted-unsent-operating-proposal'
    objects.append({'path':path,'jsonPointer':'/records/4','kind':'complete-unadopted-Corruption-Purge-proposal','value':v})
    findings=[
        {'id':'TR-01','finding':'Original Matrix P280–289 makes the Warden custodian of the Pact and the automatons extensions of that function. They protect the system rather than every adventurer and respond to threats to prison/resonance. This supports possible enforcement context, not proof that every Hunt NPC is an automaton or that patrols pursue everyone everywhere. Secondary Codex lines81/111 describes ordinary patrol limits; no exact Hunt roster is supplied.'},
        {'id':'TR-02','finding':'Core P1275 explicitly classifies soul destruction, involuntary identity alteration, Old One contact, permanent Gate rewriting, Unity resonance and Matrical execution as forbidden; casting may create evidence, attention or Pact pursuit even on success. It does not supply a deterministic automatic Hunt threshold or make all research itself a completed forbidden cast.'},
        {'id':'TR-03','finding':'Director Unity/False Resonance guidance describes loss of meaningful distinction and explicitly separates susceptibility, guilt, ordinary commerce and ordinary corruption. It does not establish that owner knowledge/proximity taint equals Unity, the Corrupted condition or a universal alignment judgment. Primordial ontology remains subject to original-source priority and explicit owner corrections.'},
        {'id':'TR-04','finding':'Instruments lines342–383 supplies secondary research-clock examples (six ticks, meaningful periods, typical DC12+tier), hidden clue strata, Rune Carving help and complications including warden attention. These are not recovered Equation fragments or approved universal progression. Sorrow-save/period conventions and the underlying architecture claim need current rules/authority reconciliation before reuse.'},
        {'id':'TR-05','finding':'Detect Corruption, Sense Corruption and Corruption Sensor use actual current explicit Corruption records/tags/states, with their own range/protection/cover/information limits. Corruption Insight reports one actual type and proximate cause, allowing Indeterminate fields. The effects do not reveal the entire Equation, an upstream Old One identity, guilt or automatic Hunt eligibility. Taint needs an explicit classification before these predicates can be applied; absence of a definition is not proof of immunity or innocence.'},
        {'id':'TR-06','finding':'Corruption Ward advantages actual qualifying saves, supplies no save where none exists, and grants neither cleansing nor immunity. Reviewed Corruption Cleanse removes one eligible ordinary Corrupted record or a qualifying minor environmental effect, not Unity/numeric tracks, past alignment shifts, intrinsic curses, knowledge or a protected cause. Do not extend it silently to erasing a Hunt or forbid its actual existing condition cure merely to preserve tension.'},
        {'id':'TR-07','finding':'Purge, Immunity and Purification remain pending ordinary spells. Full unadopted AC6-06 Purge distinguishes all eligible effects from intrinsic/protected causes and numerical tracks, with broader area removal. Immunity lacks a completed procedure; Purification retains permanent-removal wording versus Until dispelled metadata. No higher-rank cure or Hunt exception is approved by this reading.'},
    ]
    result={'reviewId':'COSMOLOGY-TAINT-RESEARCH-SOURCE-READING-04','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
            'status':'Bounded local semantic reading, unsubmitted; no rules adopted','sourceBindings':list(bindings.values()),
            'docxPassages':paras,'markdownSections':sections,'objects':objects,'findings':findings,
            'coverage':{'completeDocxParagraphs':25,'markdownSections':4,'completeCurrentSpellCards':9,'reviewedAmongThose':6,'pendingAmongThose':3,'statusEntries':3,'completeUnadoptedProposals':1,
                        'notClaimed':'Search hits elsewhere, generic creature stubs and whole manuals are not claimed semantically reviewed. Old overcasting/Burnout rows are not adopted as current magic rules.'},
            'huntRosterIdentified':False,'taintTrackMapped':False,'newMechanicsAdopted':False,'sourceInformationDeleted':0,'spellFlagsChanged':False,'fullCosmologyApproved':False}
    assert len(paras)==25 and len(sections)==4 and len(objects)==13
    target.write_bytes(encoded(result))
    for row in bindings.values():assert info(G/row['path'])==row
    check.write_bytes(encoded({'record':info(target),'sourceBindingsVerified':len(bindings),'paragraphs':25,'completeCurrentCards':9,'reviewedCards':6,'pendingCards':3,'completeUnadoptedProposal':1,'newMechanicsAdopted':False}))
    print(json.dumps(read(check)))

if __name__=='__main__':main()
