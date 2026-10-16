"""Preserve the last three original epilogue hooks and their real interface gaps."""
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def main():
    target=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARC_READING_01.json'
    assert not target.exists()
    source=G/'The Cosmology of Decennium Descent.docx'
    inv=json.loads((A/'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json').read_bytes())
    assert inv['source']==info(source)
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(source) as z:
        rows=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in ET.fromstring(z.read('word/document.xml')).findall('.//w:p',ns)]
    for unit in inv['units'][14:17]:
        for evidence in unit['evidence']:
            value=rows[evidence['paragraphIndexZeroBased']]
            assert value==evidence['text'] and hashlib.sha256(value.encode()).hexdigest()==evidence['textSha256']
    context=[]
    for i in [254,261,262,265,319,320,321,322]:
        context.append({'path':source.relative_to(G).as_posix(),'part':'word/document.xml','paragraphIndexZeroBased':i,
            'text':rows[i],'textSha256':hashlib.sha256(rows[i].encode()).hexdigest()})
    transport=R/'docs/mechanics/expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md'
    lines=transport.read_text('utf-8').splitlines();excerpt='\n'.join(lines[188:209])
    record={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'Source and dependency reading only; no arc submitted or adopted; campaign frame remains unanswered.',
        'source':info(source),'units':inv['units'][14:17],'sourceContext':context,
        'sourceUnitEvidenceChecks':6,'failureCount':0,
        'transportInterface':{'source':info(transport),'firstLineOneBased':189,'lastLineOneBased':209,
            'excerpt':excerpt,'textSha256':hashlib.sha256(excerpt.encode()).hexdigest()},
        'findings':[
            'P319 explicitly offers these three arcs to campaigns continuing beyond the epilogue. Their events are not automatically current facts in a before/during Proof War campaign.',
            'P261–265 describe the original Shard resolution, Charter of Infinite Yield, Ladder dissolution/aurora, new sky colors and continued Sentinel presence. Owner identity and chronology corrections still govern; these passages cannot identify the source Shard with Q6 or settle Ul’nak/Old God identities.',
            'P262 says the Concord spear was remelted into a thousand small pendants for children. Those pendants are not automatically the distinct Shard Pendant of Xi from P302, and their number does not create unlimited operative relic stock. P303 Concord Spear Fragment needs explicit provenance consistent with preserved source or labeled NEW adaptation.',
            'Source Yieldheart sky/city references do not establish that a current Floor1–10 Yieldheart Caverns label is the same location. Do not silently collapse names into a geographic route.',
            'P321 names sky-vessel voyages but supplies no complete craft profile. Current transport contracts require actual hull, payload, crew Actions, fuel/service, route and repair histories. Ordinary watercraft are not flying vehicles by implication.',
            'P322 names Cania engine patents and annual contradictions, but gives no executable fictional contract terms, benefit, delivery/acceptance method, deadline, refusal encounter or breach consequences. Original Mephistopheles duplication remains corrected to Cania only; this hook does not fill the Maladomini vacancy.',
        ],
        'nextConferenceQuestions':[
            {'id':'EPI-15','questions':[
                'Create a conditional post-epilogue module with exact investigation evidence, finite fragments, actors, local maps, hazards and recover/withdraw/failure outcomes. Do not globally mark the sky altered or grant free celestial travel.',
                'Define a finite NEW local Equinox deadline record using actual campaign time and notice before commitment. Do not adopt710AE as an epoch or invent universal astronomical dates. Include exact-deadline resolution and an actual failed-deadline consequence.',
                'Weaponized silence needs a complete local effect and source attribution under current Null, communication, hearing, spell-component and life rules. A recovered fragment is not automatically an Equation fragment, crafting license or limitless weapon.'
            ]},
            {'id':'EPI-16','questions':[
                'Define whether melody loss is rumor, individual condition, bounded NPC scenario or actual PC choice. Do not erase Bard class cards, personal memories, training or source records without an explicitly reviewed rule and player-facing procedure.',
                'Supply finite sky-vessel access, full craft/crew/fuel/cargo/stat/repair profiles, timed routes, altitude/environment dangers and rescue/landing choices. Use actual transport action/reservation rules and ordinary carrying limits.',
                'Retrieving a Broken Ladder strand needs defined geometry, timing, resistance, handling/storage and consequences. A named errant equation does not reveal the recovered cosmic Equation or universally remove KT/PT.'
            ]},
            {'id':'EPI-17','questions':[
                'Write the entire fictional contract as a usable handout: actual claimant selection, named issuer/authority, offered finite knowledge, exact annual obligation, delivery, acceptance, notice, opt-out/refusal and bounded breach consequences.',
                'Provide real noncoerced acceptance/refusal choices and a complete envoy scene/profile. A test of free will must not force player beliefs, demand real private facts or become an automatic Paladin Oath breach.',
                'Distinguish narrative patents from ownership/proficiency, spell unlocks, public legal authority, souls, resurrection, pacts and current feat sigils. Any new mechanical benefit requires a fixed operative envelope and cannot promote pending spells/feats.',
                'Define what counts as a submitted contradiction with finite examples and an observable adjudication rule, not a hidden Director morality test; annual is actual calendar time, not session count or everyDescent.'
            ]}
        ],
        'searchLimit':'Targeted sky-vessel/airship/Equinox/Yieldheart/BrokenLadder/engine-patent searches in current mechanics and expedition candidates; not a global absence claim.',
        'sourceInformationDeleted':0,'newRulesAdopted':False,'campaignEpochChosen':False,
        'runtimeTestsExecuted':0,'humanPlaytested':False,'wholeGameApproved':False}
    target.write_bytes(encoded(record));print(json.dumps(info(target)))

if __name__=='__main__':main()
