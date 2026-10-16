"""Preserve bounded souls/death source reading without adopting new mechanics."""
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib, json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p): return json.loads(p.read_bytes())

def main():
    target=A/'COSMOLOGY_SOULS_DEATH_SOURCE_READING_01.json'
    guide=R/'docs/director-only/cosmology/SOULS_DEATH_REVIEW_PREPARATION_01.md'
    check=A/'COSMOLOGY_SOULS_DEATH_SOURCE_READING_01_CHECK.json'
    assert all(not p.exists() for p in [target,guide,check])
    bindings={}; passages=[]; objects=[]; sections=[]
    def bind(p):
        row=info(p);bindings[row['path']]=row;return row['path']
    n={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    specs=[(G/'The Cosmology of Decennium Descent.docx',
            [55,56,58,72,73,79,103,104,106,108,109,110,111,112,113,114,115,116,117,146,147,164,165,167,183,185,188]),
           (G/'The Decennium Descent and the Matrix of Oblivion.docx',
            list(range(39,50))+list(range(160,172))+list(range(214,230))+list(range(289,304)))]
    for p,indices in specs:
        path=bind(p)
        with ZipFile(p) as z:root=E.fromstring(z.read('word/document.xml'))
        paras=[''.join(t.text or '' for t in el.findall('.//w:t',n)) for el in root.findall('.//w:p',n)]
        for i in indices:
            text=paras[i]
            passages.append({'path':path,'part':'word/document.xml','paragraphIndexZeroBased':i,
                             'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()})
    p=R/'data/public/spell_playtests/catalog.json';path=bind(p);cat=read(p)
    ids={'stitch-fate','death-ward','resurrection','mass-resurrection-denial','true-resurrection','soul-bind'}
    for i,v in enumerate(cat['spells']):
        if v['id'] in ids:
            assert v['status']=='operational-playtest-draft' and v['operational']
            objects.append({'path':path,'jsonPointer':f'/spells/{i}','kind':'complete-current-ordinary-spell','value':v})
    assert len(objects)==6
    for cls,indices in [('cleric',[29,32,37,57]),('monk',[32]),('paladin',[30,66]),('mage',[50])]:
        p=R/f'data/public/class_playtests/{cls}.json';path=bind(p);data=read(p)
        for i in indices:objects.append({'path':path,'jsonPointer':f'/cards/{i}','kind':'complete-current-class-card','value':data['cards'][i]})
    for rel,ranges in [
        ('docs/mechanics/HEALING_DEATH_PLAYTEST.md',None),
        ('docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md',[(58,87)]),
        ('docs/mechanics/CONDITIONS_PLAYTEST.md',[(188,218),(741,766)]),
        ('docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md',None),
    ]:
        p=R/rel;path=bind(p);lines=p.read_text(encoding='utf-8').splitlines()
        for lo,hi in ranges or [(1,len(lines))]:
            text='\n'.join(lines[lo-1:hi]);assert hi<=len(lines)
            sections.append({'path':path,'firstLineOneBased':lo,'lastLineOneBased':hi,'text':text,
                             'textSha256':hashlib.sha256(text.encode()).hexdigest()})
    owner=R/'data/director/cosmology/heartcell_owner_update_02.json'
    bind(owner);bind(R/'docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md')
    assert read(owner)['sourcePreferenceAmbiguityClosed'] and not read(owner)['numericalMechanicsImplemented']
    findings=[
        {'id':'SD-01','topic':'Mortal soul origin and enduring identity','finding':'Original P72 coalesces first mortal souls from Source fragments near the prison; P73 describes choice and subtle attunement without loss of agency. This does not specify a universal post-death route, return clock, identity destruction rule, or automatic rebirth.', 'sources':['Cosmology P72–73'],'remaining':'Read later soul passages and mortal plane testimony; preserve existing identity/willingness mechanics without inventing metaphysics.'},
        {'id':'SD-02','topic':'Argent Gate, judgment and historical epochs','finding':'P164 describes soul arrivals/departures. P185 introduces Seraphon’s Gate of Gentle Departures at the Argent threshold and authentic last acts, regardless of virtue. P165 concerns memory tableaux, not an exhaustive afterlife itinerary. P116’s Serit death/bloom conflicts with later alive accounts already registered.', 'sources':['Cosmology P116,164–165,185'],'remaining':'Compare the Shadow Conclave and other mortal claims after planes review. Do not make one historical gate practice a universal current soul test or silently resolve campaign epoch.'},
        {'id':'SD-03','topic':'Infernal commerce, consent and claims','finding':'Original soul contracts, identity stripping and permanent service exist; later refraction changes enforceability and yields. Matrix P297 names resurrection clauses and post-seal enforceable contracts. These establish fiction, not a blanket spell blocker, generic soul ownership mechanic, or purchased Hunt exception.', 'sources':['Cosmology P55–56,79,146–147,167,183,188','Matrix P297'],'remaining':'Read actual contract/faction procedures. Distinguish legal/body claims from an explicit operational soul-return barrier.'},
        {'id':'SD-04','topic':'Existing resurrection procedures','finding':'Six ordinary cards and eight class cards are read in full. Ordinary Resurrection requires remains and an eight-hour window; True Resurrection permits legal bodyless return within seven days. Both retain identity blockers and consequences. Soul Bind is a finite identity barrier; Mass Resurrection Denial is corpse-local. Specific class procedures remain separate.', 'sources':['Complete cards in objects','HEALING_DEATH_PLAYTEST.md'],'remaining':'Carry exact costs/access, willingness, body/formation, location, windows, anti-duplication and persistent history into the conference. No new spell approvals.'},
        {'id':'SD-05','topic':'Hunt permanence and rare intervention','finding':'The owner states Hunt initiation makes the character hardcore and death final, then expressly corrects an absolute ban: extremely rare Divine/Abyssal intervention is possible. Ordinary resurrection is not a routine escape. The owner has not supplied an operational exception list, number, payment, trigger or authority procedure.', 'sources':['HEARTCELL-OWNER-UPDATE-02 / HC02-06 and exactOwnerMessages'],'remaining':'Confer on the interface. A divine name, class tag, spell rank or infernal contract does not by itself establish the owner’s extraordinary exception; this is a proposed implementation boundary, not a newly approved mechanic.'},
        {'id':'SD-06','topic':'Prevented death versus return after death','finding':'Positive-HP floors, healing of a surviving zero-HP target, would-die replacement, actual resurrection and companion reconstruction have different existing procedures. Phoenix Rebirth heals a living target; Ritual Ward replaces eligible death before finalization; Soulbound Ritual reconstructs specific companions.', 'sources':['Complete class/ordinary cards','HEALING_DEATH_PLAYTEST.md'],'remaining':'Ask GPT to distinguish what the owner’s “if they die” wording supports from any new Hunt-specific restrictions. Do not disable all survival effects or treat a prevented death as automatically final without a source.'},
        {'id':'SD-07','topic':'Time Loop and retained knowledge','finding':'The bounded temporal kernel can restore life-state and snapshot Soul Bind with conserved absolute clocks/history; invoking Oracle and snapshot allies retain individually learned memories. Full Time Loop remains unavailable. Neither kernel nor earlier resurrection classification supplies a Hunt exception.', 'sources':['TEMPORAL_KERNEL_PLAYTEST.md'],'remaining':'Hunt initiation, research knowledge, taint and outside Pact enforcement need an explicit temporal policy before admission. Do not enable an unreviewed rewind escape or erase learned knowledge by assumption.'},
        {'id':'SD-08','topic':'Taint, Corrupted and Unity Exposure','finding':'Owner functional-knowledge taint and level-5 voice/proximity taint are qualitative directions. Existing Corrupted is a named condition and Unity Exposure a distinct provisional 0–6 track with reviewed generic recovery. Their numerical procedures do not prove either is identical to the owner’s taint.', 'sources':['HEARTCELL-OWNER-UPDATE-02','CONDITION_RECOVERY_PLAYTEST.md lines58–87','CONDITIONS_PLAYTEST.md selected sections'],'remaining':'Confer before mapping tracks, thresholds, cleansing, immunity, inherited memory, Hunt detection or seven-stage proposals. No numerical system adopted here.'},
        {'id':'SD-09','topic':'Death, cessation and public revelation','finding':'Matrix P167–171 distinguishes death as transition from cessation that ends distinction. This describes a threat; it is not complete target/save/counterplay rules or identification of Ul’nak, the primal survivor, or the Floor97 Old God.', 'sources':['Matrix P160–171,214–229','Current Q6 and owner qualifications'],'remaining':'Keep Director truth, mortal teaching and specific rules distinct; complete the related source reading before building a final souls chapter.'},
    ]
    record={'reviewId':'COSMOLOGY-SOULS-DEATH-SOURCE-READING-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
            'status':'Bounded local semantic source reading; review preparation, not a GPT verdict or adopted new rule',
            'sourceBindings':list(bindings.values()),'docxPassages':passages,'objects':objects,'markdownSections':sections,'findings':findings,
            'coverage':{'originalCosmologyParagraphs':27,'matrixParagraphs':54,'completeOrdinarySpellCards':6,'completeClassCards':8,
                        'scope':'Only listed passages/cards/sections read. Keyword discovery and truncated outputs are not whole-source semantic coverage. No complete soul corpus or whole game claim.'},
            'nextSourceReads':['Current mortal afterlife/Shadow Conclave testimony and planes verdict','Exact Research skill/library and current infernal contract/body-claim rules','Other soul/necromancy cards and source-specific blockers relevant to the selected interface','Whole current temporal parent/control contracts if their concrete operations are proposed'],
            'ordinarySpellBaseline':{'reviewed':419,'pending':429,'total':848,'changed':False},
            'newMechanicsAdopted':False,'sevenStageTaintApproved':False,'huntExceptionMechanicsApproved':False,
            'publicExportEnabled':False,'fullCosmologyApproved':False,'runtimeApproved':False,'sourceInformationDeleted':0}
    assert len(passages)==81 and len(objects)==14 and len(sections)==5
    target.write_bytes(encoded(record))
    text='''# Souls, death and the Hunt — review preparation

This is a bounded source comparison for the next GPT conference. It adds no numerical taint system, intervention procedure or new spell approval. Use [the current owner decisions](HEARTCELL_OWNER_UPDATE_02.md) and [current cosmology reading order](CURRENT_COSMOLOGY_READ_FIRST.md).

'''
    for f in findings:text+=f"## {f['id']} — {f['topic']}\n\n{f['finding']}\n\n**Still to settle:** {f['remaining']}\n\n"
    text+='''## What has actually been read

The [source record](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_DEATH_SOURCE_READING_01.json) preserves 27 complete Cosmology paragraphs, 54 Matrix paragraphs, six complete current ordinary spell cards, eight complete current class cards, the healing/death guide, the temporal kernel guide and the selected Corrupted/Unity Exposure sections. It records exact source hashes and paragraph, JSON or line locations. Broader spell catalogs, contract procedures and all soul lore are not claimed fully reviewed.

The existing public Corrupted condition and provisional Unity Exposure track must not silently become the owner's new knowledge/proximity taint. Likewise, a spell called Divine Rebirth does not establish the extremely rare Divine intervention the owner allowed. These are interfaces to discuss explicitly, not reasons to overwrite the original texts.

No sources were deleted, no public export changed, and the ordinary spell totals remain 419 reviewed / 429 pending.
'''
    guide.write_text(text,encoding='utf-8',newline='\n')
    for row in bindings.values():assert info(G/row['path'])==row
    check.write_bytes(encoded({'record':info(target),'guide':info(guide),'sourceBindingsVerified':len(bindings),
                              'docxParagraphs':len(passages),'completeObjects':len(objects),'markdownSections':len(sections),
                              'newMechanicsAdopted':False,'sourceInformationDeleted':0}))
    print(json.dumps(read(check)))

if __name__=='__main__':main()
