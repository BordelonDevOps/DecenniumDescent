"""Preserve exact life/damage interfaces needed for the next Null conference."""
from datetime import datetime,timezone
from zipfile import ZipFile
import hashlib,json,re,xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G,R,A,info,encoded

def digest(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
def excerpt(p,start,end):
    lines=p.read_text('utf-8').splitlines();text='\n'.join(lines[start-1:end])
    return {'source':info(p),'lineStartOneBased':start,'lineEndInclusive':end,'text':text,'textSha256':digest(text)}

def main():
    target=A/'COSMOLOGY_EPILOGUE_NULL_LIFE_SOURCE_FOLLOWUP_01.json';assert not target.exists()
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    book=G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx'
    with ZipFile(book) as z:root=ET.fromstring(z.read('word/document.xml'))
    rows=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in root.findall('.//w:p',ns)]
    assert rows[8282]=='When reducing a creature to 0 HP with a melee attack, you can choose to knock it out instead of killing it. It falls unconscious and is stable.'
    book_evidence=[{'source':info(book),'part':'word/document.xml','paragraphIndexZeroBased':i,'text':rows[i],'textSha256':digest(rows[i])} for i in [4238,8282,8286]]
    source=R/'data/public/class_playtests/soldier.json';cards=json.loads(source.read_text('utf-8'))['cards'];card=cards[29]
    assert card['id']=='soldier.hero.champion.sacrificial-defense'
    mechanics=R/'docs/mechanics'
    excerpts=[excerpt(mechanics/'CORE_RESOLUTION_PLAYTEST.md',35,60),excerpt(mechanics/'HEALING_DEATH_PLAYTEST.md',17,51),excerpt(mechanics/'DAMAGE_SHARING_PLAYTEST.md',49,59)]
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'source/interface preparation only; not submitted and no new rules adopted',
      'previousReading':info(A/'COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json'),
      'bookEvidence':book_evidence,'currentSourceCard':{'source':info(source),'jsonPointer':'/cards/29','record':card},'currentLifeInterfaceEvidence':excerpts,
      'findings':[
        'V6 P8282 grants optional knockout only on reducing a creature to0HP with a melee attack. It does not itself supply a universal nonlethal-damage type or general ranged/area/ongoing-damage permission.',
        'Current Core integration resolves Instant Death and fatal Wounds before the surviving melee-knockout Stable assignment. Current later healing interface adds exact survival windows; it does not make knockout an all-causes death prevention.',
        'Original cosmology P314 says all damage dealt becomes non-lethal during Null Veil. How this expands targeting/damage sources and interacts with Instant Death, Wounds, already-zero targets, Maiming and non-damage death is an actual unsolved interface, not an automatic identity with V6 knockout.',
        'Soldier Sacrificial Defense preserves the historical non-lethal phrase in provenance but its current card explicitly forbids erasing massive-damage rules. That class-specific integration is not a general definition for every Null effect.',
        'Damage sharing preserves the original attacker/hit and source lineage; transferred recipients do not inherit attack/knockout riders merely because damage moved. A Null conversion must define original damage-owner versus transferring/reflecting character and which recipient branches it affects.',
        'The source term all damage does not by itself convert non-damage HP payments, direct death, lethal Exhaustion/Strain, Hunt finality or resurrection restrictions. New Null procedures must classify these explicitly without silently merging KT/PT/Corruption/Null Veil.'
      ],
      'nextConferenceQuestions':[
        'Define exactly when Null conversion is evaluated (damage-source owner at creation or resolution, current veil suppression, delayed packets), what counts as damage the character deals, and whether companion/environmental consequences count. Preserve a single root/recipient lineage and no duplicated prevention/resource triggers.',
        'Choose and justify NEW explicit nonlethal integration for creature recipients, objects/constructs, positive-to-zero, already-zero and massive damage. If this source-specific rule prevents death/Wounds, identify the precise overridden stages; if it does not, explain why all damage non-lethal still admits fatal results. Do not hide the choice behind the generic word nonlethal.',
        'Specify whether the one-round successful CHA shrug temporarily suppresses or actually removes the Veil, what remains during suppression, exact resume/expiry marker, and duration of failed-save Incapacitated. Failure cannot indefinitely prevent the Bonus Action needed to escape without a printed recovery procedure.',
        'Keep original hourly WIS DC15 exposure, but define cumulative exposure/reentry, field identity, changing boundaries, repeat saves while already Veiled, unconscious/sleeping travelers and simultaneous exposures. A mask fear/Null-lullaby advantage does not automatically label every residual Null save a lullaby.',
        'Specify each exact purge route: mask confession action/time/understood fictional content/wearing status, which Archon blessing/Guidance/Test counts, and finite brew dose/administration/consumption. Do not assume any previously granted temporary Archon card permanently grants purge.',
        'Use numerical examples for HP10/max20 taking40, HP3/max20 taking8, a preexisting3-Wound failed save, a Stable0 victim hit again, ranged/area/delayed/shared damage, ongoing source whose Veil changed, a constructed target and direct HP cost. Keep death/Hunt decisions separate.'
      ],
      'searchLimit':'Targeted nonlethal/knockout/passive-Insight searches and exact current life interfaces only; not proof of absence from all historical sources.',
      'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'wholeGameApproved':False}
    target.write_bytes(encoded(result));print(json.dumps({'saved':info(target),'bookParagraphs':3,'currentCard':card['id'],'mechanicsExcerpts':3,'newRulesAdopted':False}))

if __name__=='__main__':main()
