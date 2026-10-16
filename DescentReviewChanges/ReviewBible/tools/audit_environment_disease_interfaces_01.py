"""Bind disease-related interfaces without inventing a disease or promoting pending content."""
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib,json,re
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    target=A/'ENVIRONMENT_DISEASE_INTERFACE_AUDIT_01.json'
    assert not target.exists()
    files={};records=[]
    def bind(p):
        v=info(p);files[v['path']]=v;return v['path']
    def record(p,pointer,value,kind):
        records.append({'kind':kind,'sourcePath':bind(p),'jsonPointer':pointer,'value':value})
    pattern=re.compile(r'disease|contagio|infect',re.I)
    books=[];ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for fn in ['Decennium_Descent_Player_Rulebook_v6.docx','Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx']:
        p=R/'books/player'/fn
        with ZipFile(p) as z:root=ET.fromstring(z.read('word/document.xml'))
        paragraphs=[''.join(t.text or '' for t in x.findall('.//w:t',ns)) for x in root.findall('.//w:p',ns)]
        matches=[{'paragraphIndexZeroBased':i,'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()} for i,text in enumerate(paragraphs) if pattern.search(text)]
        books.append({'sourcePath':bind(p),'part':'word/document.xml','paragraphCount':len(paragraphs),'matches':matches,
          'scope':'Literal all-w:p scan, including table cells. References to protection, cure and flavor are not operational disease profiles.'})
    class_scan=[]
    for p in sorted((R/'data/public/class_playtests').glob('*.json')):
        d=read(p);class_scan.append({'sourcePath':bind(p),'cardsScanned':len(d.get('cards',[]))})
        for i,c in enumerate(d.get('cards',[])):
            if pattern.search(c.get('effect','')):record(p,f'/cards/{i}',c,'current-class-disease-interface')
    p=R/'data/playtest/ancestry_background_candidate.json';d=read(p)
    for key in ['ancestries','backgrounds']:
        for i,c in enumerate(d[key]):
            if pattern.search(json.dumps(c,ensure_ascii=False)):record(p,f'/{key}/{i}',c,'ancestry-background-source-and-operational-record')
    p=R/'data/public/spell_playtests/catalog.json';d=read(p)
    for i,c in enumerate(d['spells']):
        if c['id'] in ['purify-drop','purify-food-and-drink','detect-poison','contagion','plague-wind']:
            record(p,f'/spells/{i}',c,'spell-interface-status-retained')
    p=R/'data/playtest/herbalism_recipe_candidate.json';d=read(p)
    for i,c in enumerate(d['cards']):
        if pattern.search(c.get('operational',{}).get('text','')):record(p,f'/cards/{i}',c,'reviewed-remedy-scope-not-generic-disease-cure')
    p=R/'data/director/bestiary_source_candidate_internal.json';d=read(p)
    for i,c in enumerate(d['records']):
        if pattern.search(c['source']['originalUtf8Text']):
            record(p,f'/records/{i}',c,'pending-bestiary-source-record')
            source=G/c['source']['path'];assert source.is_file()
            assert hashlib.sha256(source.read_bytes()).hexdigest()==c['source']['sha256']
            bind(source)
    guides=[]
    guide_specs={
      'CONDITIONS_PLAYTEST.md':[(500,518)],
      'HERBALISM_RECIPE_PLAYTEST.md':[(31,59)],
      'POISONCRAFTING_RECIPE_PLAYTEST.md':[(7,17),(39,49),(124,141)],
      'EQUIPMENT_ITEM_PROCEDURES.md':[(3,17)],
      'CREATURE_LIFECYCLE_PLAYTEST.md':[(21,29)]}
    for name,ranges in guide_specs.items():
        p=R/'docs/mechanics'/name;lines=p.read_text(encoding='utf-8').splitlines()
        for lo,hi in ranges:
            assert hi<=len(lines)
            excerpt='\n'.join(lines[lo-1:hi]);guides.append({'sourcePath':bind(p),'firstLineOneBased':lo,'lastLineOneBased':hi,
              'excerpt':excerpt,'textSha256':hashlib.sha256(excerpt.encode()).hexdigest()})
    findings=[
      {'id':'DIA-01','finding':'Disease, poison damage, Poisoned and an underlying poison application are distinct predicates. Neither Contagion Touch naming nor a poisonous symptom establishes a transmissible disease.',
       'evidenceSelectors':['bestiary hush-broker-plaguehand: Contagion Touch prints necrotic damage only','POISONCRAFTING_RECIPE_PLAYTEST','HERBALISM antidote operational.text'],
       'authoringRequirement':'Every new hazard must declare its actual effect tags and source identity. Do not infer contagion from a name.'},
      {'id':'DIA-02','finding':'Current class treatment includes direct cures, additional source-permitted saves, detection and immunities with different scopes. A single generic cure-disease operation would change those cards.',
       'evidenceSelectors':['crimson-agent.hero.bloodweaver.purify-blood','paladin.base.lay-on-hands','monk.hero.enlightened-master.healing-touch','warrior.hero.wardborn.stabilizing-injection','warrior.hero.ironskin.cellular-reconstruction'],
       'authoringRequirement':'Disease profiles must specify whether repeated saves exist, what an extra save changes, applicable treatment DC, magical/nonmagical classification and any special-cure restrictions. Pay the actual class costs and recharge; no cure or save is invented by generic wording.'},
      {'id':'DIA-03','finding':'Petrified suspends existing disease rather than deleting it. The existing condition says it can resume if neither expired nor cured. The next draft must settle each disease clock while suspended and honor legal cures without automatic replay.',
       'evidenceSelectors':['CONDITIONS_PLAYTEST lines500-518'],
       'authoringRequirement':'Work onset, repeat-save, suppression and expiry across Petrified ending. Preserve the source condition; distinguish an immunity preventing a new application from a cure of an existing one.'},
      {'id':'DIA-04','finding':'Detect Poison does not diagnose disease. Sacred Touch can detect a disease presence within its printed procedure without revealing origin or cure. Purify Drop expressly excludes pathogens; Purify Food and Drink removes eligible nonmagical contamination outside creatures but cannot cure an infected creature.',
       'evidenceSelectors':['detect-poison','purify-drop','purify-food-and-drink','paladin.base.sacred-touch'],
       'authoringRequirement':'Preserve separated batch, quantity, target, class/rank and detection limits. Record whether contamination is an object/food hazard or an established creature disease.'},
      {'id':'DIA-05','finding':'Contagion and Plague Wind remain blocked-pending-operational-review with no operational card. The inspected bestiary disease matches are pending source records: one Plaguehand attack name/flavor and four printed disease immunities.',
       'evidenceSelectors':['contagion','plague-wind','pending-bestiary-source-record'],
       'authoringRequirement':'Route spell effects and creature combat implementation to their actual pending conferences. A new environmental disease must be clearly NEW scene authorship; these names do not authorize importing another game’s disease rules.'},
      {'id':'DIA-06','finding':'Herbalism topical care can supply one expressly required local step in an existing infection procedure; it cannot manufacture that procedure or waive its other costs. Antidotes remove eligible Poisoned, not disease.',
       'evidenceSelectors':['HERBALISM_RECIPE_PLAYTEST lines31-59','reviewed-remedy-scope-not-generic-disease-cure'],
       'authoringRequirement':'Print any useful topical-treatment step explicitly in the new disease profile, then preserve its remaining elapsed time, checks, medicine, kit and Supply costs. Full HP does not by itself invalidate the independent topical step.'},
      {'id':'DIA-07','finding':'Ranger bonding retains pre-existing disease/poison/conditions. Temporary form immunities, genuine disease immunity and nonmagical-only immunity require their own actual scopes; creature type alone does not erase disease.',
       'evidenceSelectors':['CREATURE_LIFECYCLE_PLAYTEST lines21-29','druid.hero.rotshaper.carrion-rat-king','druid.hero.land.nature-s-ward','mage.hero.lich.undead-immunities','ranger.hero.outrider.toxic-affinity'],
       'authoringRequirement':'Work existing infection through bonding and form changes, using actual identity and clock records. Keep poison resistance and nonbreathing separate from disease protection.'},
      {'id':'DIA-08','finding':'The bounded source scan locates disease references and interfaces but does not establish a complete general environmental transmission/onset/progression/treatment framework.',
       'evidenceSelectors':['books literal scan','current-class-disease-interface','spell-interface-status-retained'],
       'authoringRequirement':'For the next NEW environmental disease candidate specify route and finite contamination source, susceptibility, initial exposure/cooldown, onset, actual symptoms, progression/repeat-save clock, failure/cure endpoints, reinfection and contact-spread permissions. Keep personal disease state separate from expedition Exposure pressure and from the unreviewed environment foundations proposal.'}
    ]
    cases=[
      'Purify Food and Drink treats one eligible separated contaminated ration before ingestion; after infection the same spell cannot cure its consumer.',
      'Purify Drop removes ordinary sediment from one legal drop but leaves pathogens; Detect Poison reports no disease diagnosis.',
      'Mundane disease and magical disease independently target Purify Blood; only the magical branch invokes its actual treatment check and failed paid attempt.',
      'Lay on Hands, Healing Touch and Stabilizing Injection face profiles with and without repeat saves; no generic instant cure or invented repeated save.',
      'Petrified begins before onset, a scheduled event occurs while suspended, a legal cure removes the record, and unpetrifying does not resurrect it.',
      'Carrion Rat King form ends with an older disease record; actual immunity scope and the ordinary body clock decide return of effects.',
      'Ranger bonds an already-infected beast; disease state and source clock remain while ordinary companion HP/lifecycle rules still apply.',
      'Topical balm heals zero at full HP but supplies exactly one explicitly permitted dressing step; other treatment costs remain.',
      'A Poisoned-only antidote removes the symptom but retains independent disease; reapplication needs the disease’s actual future trigger.',
      'Hush-Broker Contagion Touch source naming alone supplies neither an infection record nor a transmission event.',
      'A source has ordinary disease plus poison damage; nonmagical disease immunity, Poisoned immunity and poison resistance are checked separately.',
      'Rest across a disease onset/repeat-save deadline uses one elapsed timeline and does not duplicate expedition Exposure/Supply costs.'
    ]
    from collections import Counter
    counts=dict(Counter(x['kind'] for x in records));counts.update(bookParagraphs=sum(len(x['matches']) for x in books),sourceFiles=len(files),findingGroups=len(findings),requiredFutureCases=len(cases))
    for p,v in files.items():assert info(G/p)==v
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Source-linked audit and authoring requirements only; unsent, no new disease rules or adoption.',
      'coverageAreas':['DD-22'],'sourceBindings':list(files.values()),'literalSearchPattern':pattern.pattern,'books':books,'classScan':class_scan,
      'records':records,'governingExcerpts':guides,'findings':findings,'requiredFutureWorkedCases':cases,'counts':counts,
      'scopeLimits':['Literal selection is bounded to the named files, not proof of absence across the archive.','Full preserved records include historical text and source status; no historical alternate or pending creature/spell is promoted.','Required future cases are specifications, not authored or executed test results.'],
      'submitted':False,'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    target.write_bytes(encoded(result));print(json.dumps({'audit':info(target),'counts':counts,'sourceFilesUnchanged':True,'submitted':False}))

if __name__=='__main__':main()
