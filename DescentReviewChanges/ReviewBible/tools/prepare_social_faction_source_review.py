"""Preserve complete ordinary social/faction source sections; no rule adoption."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def record(p):return {'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()}
def save(p,x):p.write_text(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def docx(rel):
    with zipfile.ZipFile(G/rel) as z:raw=z.read('word/document.xml')
    body=ET.fromstring(raw).find('w:body',NS);ps=[];blocks=[];tables=0
    for bi,e in enumerate(body):
        if e.tag.endswith('}p'):
            text=''.join(n.text or '' for n in e.findall('.//w:t',NS))
            blocks.append({'kind':'paragraph','bodyElementIndex':bi,'paragraphIndex':len(ps),'text':text});ps.append(text)
        elif e.tag.endswith('}tbl'):
            rows=[[[''.join(n.text or '' for n in p.findall('.//w:t',NS)) for p in c.findall('w:p',NS)] for c in row.findall('w:tc',NS)] for row in e.findall('w:tr',NS)]
            blocks.append({'kind':'table','bodyElementIndex':bi,'afterParagraphIndex':len(ps)-1,'tableIndex':tables,'rows':rows});tables+=1
    return {'file':rel,**record(G/rel),'documentXmlSha256':sha256(raw).hexdigest(),'bodyParagraphCount':len(ps),'bodyTableCount':tables,'paragraphs':ps,'blocks':blocks}
def select(document,ranges):
    return [b for b in document['blocks'] if any(a<=b.get('paragraphIndex',b.get('afterParagraphIndex'))<z for a,z in ranges)]
def main():
    out=A/'SOCIAL_FACTION_SOURCE_PREPARATION.json'
    assert not out.exists()
    director=docx('docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx')
    mirror=docx('DescentReviewChanges/ReviewBible/docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx')
    player=docx('books/player/Decennium_Descent_Player_Rulebook_v6.docx')
    dranges=[(657,670),(765,775)]
    assert director['paragraphs'][657]=='Chapter 36 — Rival Expeditions and Faction Turns'
    assert director['paragraphs'][765]=='Chapter 44 — Social Conflict and Reputation Scenes'
    def section(doc,start,end):
        a=doc['paragraphs'].index(start);z=next(i for i,s in enumerate(doc['paragraphs']) if i>a and s==end)
        return (a,z)
    pranges=[section(player,'Reputation in Aethel','The Decennial Opening'),section(player,'Charisma Checks','Spellcasting Ability'),section(player,'Reputation and Alignment Interactions','Chapter 8: Combat in Aethel')]
    mranges=[section(mirror,'Chapter 36 — Rival Expeditions and Faction Turns','PART VI — CAMPAIGNS ACROSS THE CYCLE'),section(mirror,'Chapter 44 — Social Conflict and Reputation Scenes','Chapter 45 — Directing Advanced and Deep-Tier Expeditions')]
    mainblocks=select(director,dranges);mirrorblocks=select(mirror,mranges)
    # The title of the next chapter is excluded; compare semantic content in order.
    def content(blocks):return [{'kind':b['kind'],**({'text':b['text']} if b['kind']=='paragraph' else {'rows':b['rows']})} for b in blocks]
    assert content(mainblocks)==content(mirrorblocks),'Review copy differs; preserve and adjudicate before equivalence claim'
    sources={}
    def add(p):sources[p.relative_to(G).as_posix()]=record(p)
    for x in [director,mirror,player]:add(G/x['file'])
    for rel in ['docs/mechanics/CORE_RESOLUTION_PLAYTEST.md','docs/mechanics/CONDITIONS_PLAYTEST.md','docs/mechanics/CLASS_PLAYTEST_RULES.md','docs/mechanics/COMBAT_ACTION_PLAYTEST.md','docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md','docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md','docs/mechanics/REPUTATION.md','docs/mechanics/GAMEPLAY_LOOP_CANON.md','docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md','docs/mechanics/ANCESTRY_BACKGROUND_REVIEW_STATUS.json','docs/playtest/SESSION_ZERO_PLAYTEST.md','data/playtest/ancestry_background_candidate.json','data/playtest/character_foundation.json','data/public/spell_playtests/catalog.json','data/public/spell_playtests/candidate_low_rank_136.json','data/public/spell_playtests/authored_review_index.json','src/data/reputation.js','src/lib/character-storage.js','src/components/ReputationPanel.tsx','src/components/CharacterBuilder.tsx']:
        add(R/rel)
    for name in ['EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json','DIRECTOR_TABLECRAFT_SOURCE_PREPARATION.json','REPUTATION_PRESERVATION_SOURCE_ADDENDUM.json','REPUTATION_PRESERVATION_RUNTIME_PROBES.json','LANGUAGE_EXACT_FULFILLMENT.json','ONBOARDING_CHARTER_EXACT_FULFILLMENT.json','LOW_RANK_136_EXACT_FULFILLMENT.json']:
        add(A/name)
    classfiles=[p for p in sorted((R/'data/public/class_playtests').glob('*.json')) if p.name!='manifest.json']+[R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json']
    assert len(classfiles)==17
    classfacts=[]
    for p in classfiles:
        add(p);data=read(p)
        assert isinstance(data['cards'],list)
        classfacts.append({'file':p.relative_to(G).as_posix(),'fullCardCount':len(data['cards']),'existingStatus':data.get('status'),'newApproval':False})
    assert sum(r['fullCardCount'] for r in classfacts)==1223
    questions=[
      ('SO-01','Declare the scene before rolling','Keep the Director Want/Leverage/Limit/Clock/Witness frame. Specify the actual requested outcome, who can decide it, available offer/threat, genuine opportunity and disclosed consequence. Define when no check is needed or no current approach can obtain the requested concession; a high roll does not create authority, knowledge or a missing prerequisite.',['D44']),
      ('SO-02','Three narrative results and four native task degrees','The manual asks for full success, costly success and refusal/reversal. Reviewed Core uses four fixed-DC task degrees with natural shifts and separate opposed-total ties. Decide exactly which roll procedure applies and how each actual result selects a predeclared narrative outcome. Do not import automatic natural20 obedience, extra degree benefits, hidden tie modifiers or binary-save critical rules.',['D44','CORE']),
      ('SO-03','Skills and actual information','Preserve Persuasion/willingness, Deception/believed information, Intimidation/perceived risk and Insight/understanding, while accounting for actual Performance and Reputation skills in the Player source and20-skill foundation. Define fixed DC versus opposed checks and limits of truthful information, misunderstanding, credible threats and investigation. Insight is not a generic lie detector; identify any proposed completion as NEW.',['D44','P-CHARISMA']),
      ('SO-04','Third reputation table and automatic modifier routing','Extend existing FL-23 with the actual Player Revered+5/Respected+3/Friendly+1/Neutral0/Suspicious-1/Hostile-3/Hated-5 modifier table, whose labels differ from the Loop standing/access table and runtime bands. Settle standing-based access versus an added check modifier, and whether Reputation skill proficiency is a distinct source so standing is not accidentally counted twice. Preserve original scores and labels.',['P-MODIFIERS','FL-23','RP-ADDENDUM']),
      ('SO-05','Alignment paragraph receipt and pre-push boundary','The adjacent original Player paragraph gives identical/compatible/opposing alignment advantage rules and incompatible terminology. Preserve the entire paragraph as evidence without interpreting cosmic alignment or inventing a compatibility chart. Identify any already reviewed controlling decision; otherwise explicitly route unresolved meanings to the post-push review and give the ordinary social procedure an honest dependency boundary. Do not infer a new universal social bonus from alignment lore.',['P-MODIFIERS','SESSION-ZERO']),
      ('SO-06','Communication, participation and elapsed time','Apply fulfilled LAX hearing/speech/signed/textual/interpretation and six-second in-encounter limits. Define one scene clock across speakers, interpreters and physically separate participants; roleplay length is not automatic fictional elapsed time. Actual language, sensory and source-specific comprehension prerequisites still apply. Silence, incapacity or a blocked channel cannot be erased by a social skill roll.',['LAX','D44']),
      ('SO-07','Assistance, repetition and changed leverage','Define eligible assistance and group participation under the current Help/action rules, and whether a second attempt with unchanged facts is available. One scene should not become unlimited independent retries by rotating speakers. State what genuinely changed evidence, cost, deadline or approach makes another attempt meaningful; preserve paid resources and prior consequences.',['COMBAT','D44']),
      ('SO-08','Social magic and source-specific agency','Carry actual Charmed/Frightened limits, fulfilled spell procedures and each acquired class feature in full. Charmed alone is not obedience or consent; intimidation is not automatically Frightened. Source-specific magical control retains its own eligibility, cost, save, ending, awareness and immunity rules. Keep remaining pending spells unavailable and avoid promoting class/card comparison records. Identify exact named hook conflicts for a separate disposition.',['CONDITIONS','LRX','CLASSES']),
      ('SO-09','NPC agreement and player table boundaries','Preserve actual authority, non-negotiable limits and the reviewed Session Zero agreement when characters bargain, threaten or disagree. Separate fictional pressure from a player table agreement and from explicit willing-recipient requirements on effects. A social result must not manufacture a resource, bind an absent owner or override the actual consent prerequisite of another procedure.',['D44','SESSION-ZERO','LAX']),
      ('SO-10','Witnesses, attributed events and standing changes','The Director changes standing after public, significant, attributable actions and distinguishes one NPC relationship from a faction. The Loop also gives scene-based numeric caps. Route numeric resolution to FL-23 and its preservation addendum; complete actual witness/evidence/event recording, timing and independent faction responses without assuming every rumor is true or globally known.',['D44','FL-23','RP-ADDENDUM']),
      ('SO-11','Faction-turn cadence and paid world actions','The manual gives up to three watched factions one action after each return to Haven/surface. Define the genuine event, fictional interval, eligibility, repeat-return guard and what actual resources/access an action requires. Rival actions must use actual routes/information/time. Prevent repeated boundary crossings or one actor on two fronts from generating free faction actions; distinguish a Director abstraction from simulated runtime.',['D36','FL-03','DR-14']),
      ('SO-12','Rival clocks and usable faction records','Retain the full rival sheet and Depth4–8/Claim4/Grudge4/Collapse4–6 source clocks. Supply finite trigger, tick amount, duplicates, completion and visible-consequence rules; a tick cannot authenticate secret information or erase a real journey. Distinguish44 generic runtime standing IDs from actual named institutions/Expeditions with goals, resources and relations. Produce a source-linked scene/faction record and full ordinary worked sequence. No new world faction history or cosmological truth follows from these fields.',['D36','RP-ADDENDUM']),
    ]
    blocks=[{'id':'D36-D44','source':director['file'],'ranges':dranges,'indexConvention':'zero-based direct body paragraphs; half-open ranges; full intervening tables retained','blocks':mainblocks},{'id':'P-SOCIAL','source':player['file'],'ranges':pranges,'indexConvention':'same zero-based direct body convention','blocks':select(player,pranges)}]
    packet=read(A/'TEACHING_NAVIGATION_EXACT_V1_PREPARATION.json');n=0
    for rel,e in packet['manifest'].items():
        if rel=='README_TEACHING_EXACT_V1.md':continue
        assert record(G/rel)==e,rel;n+=1
    result={'status':'prepared-unsent-social-and-faction-source-conference','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Ordinary social scenes, institutional standing interfaces and rival/faction turn procedures. Not full setting, historical eras or cosmology review. No new mechanic or current source change.','questions':[{'id':i,'title':t,'question':q,'sourceGroups':refs} for i,t,q,refs in questions],'sourceDocuments':[{k:v for k,v in d.items() if k not in ['paragraphs','blocks']} for d in [director,mirror,player]],'selectedSourceBlocks':blocks,'directorMirrorComparison':{'mainRanges':dranges,'mirrorRanges':mranges,'completeSelectedParagraphAndTableTextEqual':True,'paragraphs':sum(b['kind']=='paragraph' for b in mainblocks),'tables':sum(b['kind']=='table' for b in mainblocks)},'fullClassComparisons':classfacts,'fullSourceFiles':sources,'allSourceHashesUnchanged':True,'activeTeachingDiskPayloadsUnchanged':n,'sourceFilesModified':0,'classCardsPromoted':0,'spellCardsPromoted':0,'runtimeImplemented':False,'humanTested':False,'cosmologyReviewed':False,'submissionStatus':'UNSENT'}
    save(out,result)
    guide=['# Social scenes and faction turns — complete selected source audit','','**Prepared and unsent.** Twelve questions preserve the actual social and faction-turn procedures instead of assuming they are absent. No source or mechanic has been changed. This is an internal source-review preparation, not a playable new social rulebook.','','[Full exact source blocks, tables and evidence inventory](SOCIAL_FACTION_SOURCE_PREPARATION.json) · [Data-preservation addendum to FL-23](REPUTATION_PRESERVATION_SOURCE_ADDENDUM.md)','','The Director social chapter supplies Want/Leverage/Limit/Clock/Witness, three narrative outcomes, differentiated social skills and witnessed reputation changes. Its rival chapter supplies a complete expedition sheet, up to three watched faction actions after a return, four named clocks and actual information/travel limits. Main and ReviewBible copies have identical complete text for these selected paragraphs and tables; the rest of their differing books is unadjudicated.','','The Player book supplies five named Charisma skills and a separate seven-band reputation modifier table. That third table is additional evidence for FL-23, not a replacement chosen by this audit. The adjacent alignment paragraph is preserved without interpreting cosmic meaning or making a compatibility chart. Current Core rolls, conditions, LAX communication, Session Zero and LRX procedures remain controlling within their already reviewed scopes. All17 complete class collections/1223 cards are included by full source path/hash for scoped comparison; no additional class promotion follows.','','| Question | Decision needed |','|---|---|']
    for i,t,q,refs in questions:guide.append(f'| {i}: {t} | {q} |')
    guide += ['','Confer after the current nine-artifact teaching review. Resolve shared numeric reputation only once with FL-23. Source chronology, faction lore, cosmic alignment, divine/planar meanings and deep-ending causes remain outside this preparation. All217 current disk payloads of that218-file teaching submission are unchanged.','']
    save(A/'SOCIAL_FACTION_SOURCE_AUDIT.md','\n'.join(guide))
    print(json.dumps({'questions':12,'fullSourceFiles':len(sources),'directorParagraphs':result['directorMirrorComparison']['paragraphs'],'directorTables':result['directorMirrorComparison']['tables'],'playerParagraphs':sum(b['kind']=='paragraph' for b in blocks[1]['blocks']),'fullClassCards':1223,'teachingPayloadsUnchanged':n}))
if __name__=='__main__':main()
