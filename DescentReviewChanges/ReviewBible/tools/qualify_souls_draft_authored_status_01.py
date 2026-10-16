"""Correct a stale Soul Mirror catalog inference and verify all draft citations."""
from copy import deepcopy
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def ptr(value,pointer):
    for part in pointer.lstrip('/').split('/'):
        part=part.replace('~1','/').replace('~0','~');value=value[int(part)] if isinstance(value,list) else value[part]
    return value

def main():
    correction=A/'COSMOLOGY_SOULS_DEATH_AUTHORED_STATUS_CORRECTION_01.json'
    check=A/'COSMOLOGY_SOULS_DEATH_HUNT_DRAFT_01_CITATION_CHECK.json'
    preserved=A/'before-souls-authored-status-correction-01'
    assert all(not p.exists() for p in [correction,check,preserved])
    draft=R/'data/director/cosmology/souls_death_hunt_conference_draft_01.json'
    chapter=R/'docs/director-only/cosmology/SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md'
    original_check=A/'COSMOLOGY_SOULS_DEATH_HUNT_DRAFT_01_CHECK.json'
    index=R/'data/public/spell_playtests/authored_review_index.json'
    candidate=R/'data/public/spell_playtests/candidate_low_rank_136.json'
    approval=A/'LOW_RANK_136_EXACT_FULFILLMENT.json'
    idx=read(index);cand=read(candidate);receipt=read(approval)
    assert idx['authoredCounts']=={'reviewed':419,'pending':429}
    approved=receipt['finalArtifacts'][candidate.relative_to(G).as_posix()]
    actual=info(candidate);assert actual['bytes']==approved['bytes'] and actual['sha256']==approved['sha256']
    entry_i=next(i for i,x in enumerate(idx['entries']) if x['id']=='soul-mirror');entry=idx['entries'][entry_i]
    assert entry['authoredStatus']=='reviewed-authored-operational-playtest' and entry['wholeCardPointer']=='/spells/124'
    card=cand['spells'][124];assert card['id']=='soul-mirror' and card['selectionEnabled'] is False
    prior=read(draft);changed=deepcopy(prior)
    selected=set()
    for n in ['COSMOLOGY_SOULS_DEATH_SOURCE_READING_01.json','COSMOLOGY_SOULS_DEATH_INTERFACE_READING_02.json','COSMOLOGY_TAINT_RESEARCH_SOURCE_READING_04.json']:
        for x in read(A/n)['objects']:
            if x['path'].endswith('spell_playtests/catalog.json'):selected.add(x['value']['id'])
    current=[x for x in idx['entries'] if x['id'] in selected]
    assert len(current)==23 and sum(x['authoredStatus']=='reviewed-authored-operational-playtest' for x in current)==14
    corrected={'reviewId':'COSMOLOGY-SOULS-DEATH-AUTHORED-STATUS-CORRECTION-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'supersedesInferencesIn':info(A/'COSMOLOGY_SOULS_DEATH_INTERFACE_READING_02.json'),
        'specificCorrection':'SD2-05 incorrectly described Soul Mirror as pending from its deliberately preserved legacy catalog. Current authored index and exact-approved standalone card prove its complete authored procedure is reviewed. Legacy catalog bytes/status remain unchanged. The earlier check’s pendingStillPending7 is only the legacy view, not current authorship; for those eight identities the current authored split is2reviewed/6pending.',
        'currentOrdinaryBaseline':idx['authoredCounts'],'combinedSelectedOrdinaryIdentities':23,'combinedCurrentAuthoredReviewed':14,'combinedCurrentAuthoredPending':9,
        'sources':[info(index),info(candidate),info(approval)],'indexLocation':{'path':info(index)['path'],'jsonPointer':f'/entries/{entry_i}','value':entry},
        'currentCompleteCard':{'path':info(candidate)['path'],'jsonPointer':'/spells/124','value':card},
        'completeSharedRulesRead':{'path':info(candidate)['path'],'jsonPointer':'/sharedRules','value':cand['sharedRules']},
        'currentCandidateMatchesExactApproval':True,'semanticQualification':'Soul Mirror is a finite one-shot return of an eligible sole-recipient ordinary spell to its original caster under LR-G14, not soul custody or an afterlife rule. Original caster/cost/concentration and one-root boundaries remain; runtime selection is not enabled.',
        'selectedCurrentAuthoredEntries':current,'historicalRecordOverwritten':False,'newSpellPromotions':0,'newRulesAdopted':False,'sourceInformationDeleted':0}
    correction.write_bytes(encoded(corrected))
    for p in [draft,chapter,original_check]:
        dest=preserved/p.name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
    preservation=[{**info(p),'preservedCopy':(preserved/p.name).relative_to(G).as_posix()} for p in [draft,chapter,original_check]]
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    changed['currentStatusCorrection']=info(correction)
    changed['sourceBindings'].extend(info(p) for p in [index,candidate,approval])
    changed['evidence']['SOUL_MIRROR_CURRENT']=corrected['currentCompleteCard']
    changed['evidence']['LOW_RANK_SHARED']=corrected['completeSharedRulesRead']
    changed['evidence']['CURRENT_AUTHORED_SOUL_MIRROR']=corrected['indexLocation']
    changed['currentSelectedSpellStatus']={'identities':23,'authoredReviewed':14,'authoredPending':9,'runtimePromotions':0}
    changed['casebook'][1]['situation']='A creature hears the voices on Descent level5 or deeper without having found a manuscript.'
    draft.write_bytes(encoded(changed))
    text=chapter.read_text(encoding='utf-8').replace('A creature hears the voices below Descent level5 without having found a manuscript.','A creature hears the voices on Descent level5 or deeper without having found a manuscript.',1)
    text=text.replace('spells remain419reviewed/429pending','spells remain 419 reviewed / 429 pending').replace('The20 cases','The 20 cases')
    text+='\n### Current spell-status correction\n\nThe [authored-status correction](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_DEATH_AUTHORED_STATUS_CORRECTION_01.json) supersedes the earlier source comparison’s statement that Soul Mirror was pending. Its complete standalone procedure is reviewed and matches the exact approved artifact; the older catalog deliberately preserves its prior pending state. Soul Mirror reflects one eligible spell under its actual rules and grants no soul custody. Across the 23 ordinary identities read for this conference, the current authored split is 14 reviewed / 9 pending. No procedure or runtime selection was promoted by this correction.\n'
    chapter.write_text(text,encoding='utf-8',newline='\n')
    # Resolve each evidence location against the actual bound source bytes, not merely its summary.
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};docx={};json_cache={};verified=[]
    for key,e in changed['evidence'].items():
        p=G/e['path']
        if 'paragraphIndexZeroBased' in e:
            if e['path'] not in docx:
                with ZipFile(p) as z:root=E.fromstring(z.read(e['part']))
                docx[e['path']]=[''.join(t.text or '' for t in v.findall('.//w:t',ns)) for v in root.findall('.//w:p',ns)]
            assert docx[e['path']][e['paragraphIndexZeroBased']]==e['verbatim']
        elif 'jsonPointer' in e:
            if e['path'] not in json_cache:json_cache[e['path']]=read(p)
            assert ptr(json_cache[e['path']],e['jsonPointer'])==e['value']
        else:
            lines=p.read_text(encoding='utf-8').splitlines()
            assert '\n'.join(lines[e['firstLineOneBased']-1:e['lastLineOneBased']])==e['verbatim']
        verified.append({'evidenceId':key,'sourceLocationResolved':True,'exactSourceValueMatches':True})
    assert len(verified)==48
    for row in changed['sourceBindings']:assert info(G/row['path'])==row
    check.write_bytes(encoded({'draft':info(draft),'chapter':info(chapter),'correction':info(correction),
        'preservationManifest':info(preserved/'PRESERVATION_MANIFEST.json'),'sourceBindingsVerified':len(changed['sourceBindings']),
        'evidenceLocationsVerified':len(verified),'evidenceChecks':verified,'sections':12,'casebookSituations':20,
        'selectedOrdinaryIdentities':23,'authoredReviewed':14,'authoredPending':9,'wholeCatalogReviewed':419,'wholeCatalogPending':429,
        'newRulesAdopted':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'check':info(check),'draft':info(draft),'chapter':info(chapter),'evidenceLocations':48,'sourceBindings':len(changed['sourceBindings']),'authoredReviewed':14,'authoredPending':9}))

if __name__=='__main__':main()
