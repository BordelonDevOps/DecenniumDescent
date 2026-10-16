"""Record actual weapon source and targeted creature/flora discovery limits."""
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
    target=A/'COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json';assert not target.exists()
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    def paragraphs(p):
        with ZipFile(p) as z:return [''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in E.fromstring(z.read('word/document.xml')).findall('.//w:p',ns)]
    book=G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx';ps=paragraphs(book)
    weapon=[]
    for ix in [6741,6743,6749,6755,6757,6759]:
        t=ps[ix];weapon.append({'path':book.relative_to(G).as_posix(),'part':'word/document.xml','paragraphIndexZeroBased':ix,'excerpt':t,'textSha256':hashlib.sha256(t.encode()).hexdigest()})
    cat=R/'data/playtest/equipment_source_catalog.json';acq=R/'data/playtest/equipment_acquisition_candidate.json'
    c=json.loads(cat.read_bytes());a=json.loads(acq.read_bytes());assert c['records'][74]['id']==a['items'][26]['id']=='simple-melee-weapons.spear'
    exact=[{'path':cat.relative_to(G).as_posix(),'jsonPointer':'/records/74','value':c['records'][74]},{'path':acq.relative_to(G).as_posix(),'jsonPointer':'/items/26','value':a['items'][26]}]
    paths=[G/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',G/'books/director/Decennium_Descent_Directors_Sealed_Bestiary_v1.docx',R/'data/director/bestiary_source_candidate_internal.json',R/'data/playtest/bestiary_public_source_candidate.json',R/'data/director/herbalism_recipe_candidate_internal.json',R/'data/director/alchemy_recipe_candidate_internal.json']
    terms=['silence wraith','echo doppelganger','bittersap','tranquil thorn','echo lily','black hush','concord spear','shard pendant']
    scans=[]
    for p in [book]+paths:
        text='\n'.join(paragraphs(p)) if p.suffix=='.docx' else p.read_text(encoding='utf-8-sig')
        scans.append({'source':info(p),'queryTerms':terms,'caseInsensitiveCounts':{t:text.lower().count(t) for t in terms}})
    target.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'source discovery and interface preparation only; no new rule adoption','previousReading':info(A/'COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json'),'weaponPropertyEvidence':weapon,'spearEvidence':exact,'targetedSearches':scans,'findings':[
      'The actual V6 Finesse rule permits STR or DEX, using the same modifier for attack and damage. Heavy imposes disadvantage for Small creatures. The properties can coexist; Finesse does not cancel Heavy. Versatile does not itself mean Two-Handed.',
      'Actual mundane Spear source:1d6piercing,Thrown20/60,Versatile1d8,3lb,baseline1gp. This is not an already-approved Concord Spear Fragment profile or price. Any inheritance into the relic must be explicit NEW integration.',
      'Soldier attunement eligibility in the original relic does not itself grant spear proficiency; the current Soldier foundation grants repeating heavy crossbows and actual sidearms. A usable relic procedure must distinguish legal wielding from proficiency and preserve the actual class foundation.',
      'No named Silence Wraith/Echo Doppelganger/Null-flora/relic identity was found in the inspected current bestiary/Alchemy/Herbalism candidate text or the three inspected books by these exact terms. Original cosmology retains those names; this search is not proof of absence from all archives or differently named material.',
      'The next EPI08–14 conference must supply complete source-qualified or explicitly NEW encounter profiles and finite flora units/access. It must not silently promote the entire pending bestiary or expand687reviewedrecipes by count alone.'
    ],'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'wholeGameApproved':False}))
    print(json.dumps({'receipt':info(target),'propertyParagraphs':len(weapon),'spearRecords':len(exact),'targetedSourceFiles':len(scans),'newRulesAdopted':False}))

if __name__=='__main__':main()
