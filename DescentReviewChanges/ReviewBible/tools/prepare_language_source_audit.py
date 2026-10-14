"""Prepare a finite DD-46 source conference without inventing language rules."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, zipfile, xml.etree.ElementTree as ET

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
PAT=re.compile(r'\blanguages?\b|\btelepath\w*|\bcommunicat\w*|\bsilen(?:ce|t)\b|\bdeafen\w*|\bspeak\w*|\bspoken\b|\bverbal\b|\bdruidic\b|\bcant\b',re.I)
TRAINING=re.compile(r'^Training$|^Downtime|learn\w*.{0,100}\blanguage|\blanguage.{0,100}(?:learn|train)|\bliteracy\b|\bliterate\b',re.I)
CASES=[
('LA-01','Starting grants and table descriptions','Keep each actual ancestry/background grant visible. Decide whether descriptive language-table population labels grant any extra proficiency. Resolve the Troll Giant/Trollish and Mycelian regional-choice/Mycelic distinctions explicitly rather than silently adding or replacing languages.'),
('LA-02','Names, aliases and dialects','Decide mechanical identity for Orc/Orcish; retain the explicit Mycelic/Sporetongue and Imperial/Common table wording. Do not equate Deep Cant, Deep Speech, Murkish, Forgotten Script, Runic or Resonant Cant merely from related names. Preserve originals and produce a literal alias/dialect map with bounded unresolved entries.'),
('LA-03','Variant precedence','Check all45 variant records against14 base grants, including Deep Dwarf, Umbrin and regional choices. State exactly when a variant adds, replaces or leaves a language; descriptive ancestry associations alone are not new grants.'),
('LA-04','Speaking, reading, writing and scripts','The14 base language traits explicitly include speak/read/write; background rows usually name languages only. Decide background literacy, script-sharing versus understanding, Gnomish and Orc use of Dwarvish script, and how script-only sources work without inventing universal script knowledge.'),
('LA-05','Choices, duplicates and availability','Set finite rules for choosing one/two languages, regional and exotic restrictions, overlapping base/background grants and later duplicates. State whether replacement is permitted and who establishes an available ordinary choice; never grant a secret tongue merely because a menu is open-ended.'),
('LA-06','Ordinary learning and downtime','Supply a usable ordinary learning procedure if no controlling current procedure is found, labelled NEW. Resolve active time, teachers/materials, interruption, cost and completion; compare pending Quick Learner\'s30-day/once-per-category source without importing that unapproved feat as the universal rule.'),
('LA-07','Translation, deciphering and research','Distinguish understanding known speech/text, translating a known script, deciphering an unknown dialect/code and research. Supply bounded Director difficulty/outcome guidance; no Intelligence/Lore success automatically grants permanent proficiency or hidden meaning. Compare Diligent Researcher and Polyglot only as pending sources.'),
('LA-08','Communication during action resolution','Bind short speech, signs, interpreting and lengthy exchanges to current turn/task procedures. Separate the player\'s accessible communication method from the character\'s fictional capacity. Decide when interpretation costs time or an Action and whether relay delay matters.'),
('LA-09','Silence, hearing and spell components','Use current conditions and spell-component authority for speech, hearing, Silenced/Deafened, verbal components and audible instructions. Telepathy does not automatically substitute for a verbal component. Resolve overlapping silence effects by their actual approved predicates.'),
('LA-10','Reviewed spell and ancestry procedures','Keep the complete current Comprehend Languages, Message and ancestry communication procedures unless a concrete conflict requires change. State comprehension versus speaking/writing, literal meaning versus codes, range/line/recipient restrictions and what knowledge persists when an effect ends.'),
('LA-11','Pending communication spells','The exact selected ordinary spell originals/current records are comparison evidence. Map Telepathy, Magic Mouth, Magic Thread, Awaken, Speak with Dead and related effects to their existing focused spell questions. Do not approve an unseen spell card or import another game\'s implementation.'),
('LA-12','Class and oath interactions','Review actual Druidic, Oracle Tongues/Ancestor, hearing/communication features and Paladin Silence/Dominion/Oathbreaker predicates. Give exact card mappings for language requirements, willing recipients, comprehension and suppression; shared names do not merge powers or change preserved oath text.'),
('LA-13','Pending feat interfaces','Eight directly matched feat originals include Linguist, Polyglot, Prodigy, Quick Learner, Telepathic, Aberrant Mind, Cold Reader and Diligent Researcher. Resolve only their comparison boundaries here; their pending dedicated feat review retains all numeric/access decisions.'),
('LA-14','Scribing, runes and written devices','Refresh after the active advanced167 verdict. Reconcile an actual Lexicon/manual/map, stored spell text, rune instructions and device command language with that verdict. Do not turn material labels or diagrams into languages or grant access from possessing an unread document.'),
('LA-15','Record keeping and companion parity','Specify the authored character record needed for exact language identity, mode, dialect, provenance, choices, temporary comprehension and training progress. Current runtime arrays remain preserved alternatives until explicitly reconciled; do not silently rewrite saves or public datasets.'),
('LA-16','Cosmology and hidden-language boundary','Preserve literal special-language names and restrictions as receipt-only where interpretation depends on cosmology. The Voice, Resonant Cant and incidental origin/setting references do not authorize pre-push cosmology review. Finish ordinary procedures and list the precise deferred question without creating origin, access or translation lore.')
]

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.resolve().relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def decode(p,marker):return json.JSONDecoder().raw_decode(p.read_text(encoding='utf-8').split(marker,1)[1])[0]

def main():
    pp=A/'LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json'
    archive=A/'DD_Language_Communication_Source_Prepared_v1.zip'
    assert not pp.exists() and not archive.exists(), 'Preserve existing snapshots'
    source=G/'docs/reference/Player_Rulebook_v6_source_text.txt';lines=source.read_text(encoding='utf-8').splitlines()
    book=R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx'
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(book) as z: xml=ET.fromstring(z.read('word/document.xml'))
    paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:p',ns)]
    indices={}
    for i,p in enumerate(paras):indices.setdefault(p,[]).append(i)
    start=[i for i,l in enumerate(lines) if l=='Languages' and i>5000];assert len(start)==1
    end=lines.index('Backgrounds',start[0])
    chapter=[{'sourceLine':i+1,'text':lines[i],'actualDocxParagraphs':indices[lines[i]]} for i in range(start[0],end) if lines[i].strip()]
    assert len(chapter)==24
    ancestry_file=R/'data/playtest/ancestry_background_candidate.json';anc=read(ancestry_file)
    assert sha(source)==anc['source']['sha256'] and len(anc['ancestries'])==14 and len(anc['backgrounds'])==20
    ancestry_grants=[];background_grants=[]
    for a in anc['ancestries']:
        traits=[t for t in a['traits'] if t['name']=='Languages'];assert len(traits)==1
        for t in traits:assert t['text'] in lines[t['sourceLine']-1] and lines[t['sourceLine']-1] in indices
        ancestry_grants.append({'ancestryId':a['id'],'name':a['name'],'fullCurrentAncestryRecord':a,'exactLanguageTrait':traits[0]})
    for b in anc['backgrounds']:
        evidence=[x for x in b['source'] if x['text'].startswith('Languages:')]
        for x in evidence:assert lines[x['line']-1]==x['text'] and x['text'] in indices
        assert bool(evidence)==('languagesSource' in b)
        background_grants.append({'backgroundId':b['id'],'fullCurrentBackgroundRecord':b,'languageFieldPresent':'languagesSource' in b,'languageEvidence':evidence})
    catalog_file=R/'data/public/spell_playtests/catalog.json';cat=read(catalog_file)
    include={'message','concordant-mindlink','omen-whisper','resonance-whisper','calm-whispers','whispers-from-beyond'}
    selected=[x for x in cat['spells'] if PAT.search(json.dumps(x['source']['original'],ensure_ascii=False)) or x['id'] in include]
    coverage=read(A/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json'); routing={}
    files={source,book,ancestry_file,catalog_file,R/'src/data/spells.js',R/'data/playtest/spell_sources/catalog.json',R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'}
    for fn in coverage['cohortFiles']:
        prep=read(A/fn)
        for s in prep['selectedSpells']:
            if s['spellId'] in {x['id'] for x in selected}:
                assert s['fullSourceAndCurrentAccessRecord']==next(x for x in selected if x['id']==s['spellId'])
                routing[s['spellId']]={'preparationFile':rel(A/fn),'questionId':s['questionId']};files.add(A/fn)
    assert all(x['id'] in routing for x in selected if x['operational'] is None)
    cm=read(R/'data/public/class_playtests/manifest.json');class_records=[]
    for c in cm['classes']:
        p=(R/'docs/mechanics'/c['data']).resolve();data=read(p)
        cards=[x for x in data['cards'] if PAT.search(x['effect']) or re.search('tongues|druidic|cant',x['id'],re.I)]
        if cards:
            files.update([p,(R/'docs/mechanics'/c['guide']).resolve(),R/'data/playtest/class_sources'/(c['class'].lower().replace(' ','-')+'.json')])
            class_records.append({'class':c['class'],'file':rel(p),'sha256':sha(p),'cards':cards,'engineFieldPresent':'engine' in data,'engine':data.get('engine')})
    feat_file=R/'src/data/feats.js'; feats=decode(feat_file,'export const feats = ')
    selected_feats=[x for x in feats if re.search(r'\blanguages?\b|\btelepath\w*|\bliteracy\b',x.get('effect',''),re.I)]
    assert len(selected_feats)==8;files.add(feat_file)
    runtime=[]
    for fn,marker in [('races.js','export const races = '),('builder-races.js','export const builderRaces = ')]:
        path=R/'src/data'/fn;rows=decode(path,marker);files.add(path)
        runtime.append({'file':rel(path),'sha256':sha(path),'rows':[{'id':x.get('id'),'name':x['name'],'languagesFieldPresent':'languages' in x,'languages':x.get('languages')} for x in rows]})
    guides=['ANCESTRY_BACKGROUND_PLAYTEST.md','ANCESTRY_SPELL_SUPPLEMENT_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CRAFTING_HARVEST_PLAYTEST.md']
    files.update(R/'docs/mechanics'/n for n in guides)
    files.update([R/'data/playtest/ancestry_spell_supplement_candidate.json',R/'data/playtest/ancestry_spell_grants_candidate.json',R/'data/playtest/spell_drafts/batch_ancestry_dependencies.json'])
    files.update((R/'data/playtest/spell_drafts').glob('*.json'))
    files.update([A/'ADVANCED_CRAFT_SOURCE_PREPARATION.json',A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json',A/'CRAFTING_FEAT_INTERFACE_PREPARATION.json',A/'SKILL_FEAT_SOURCE_PREPARATION.json',A/'GENERAL_EXPLORATION_FEAT_SOURCE_PREPARATION.json',A/'MAGIC_EXTENDED_FEAT_SOURCE_PREPARATION.json',Path(__file__)])
    assert all(p.is_file() for p in files),[rel(p) for p in files if not p.is_file()]
    protected={rel(p):sha(p) for p in sorted(files,key=rel)}
    report={'status':'source preparation only; UNSENT; no language mechanics approved','preparedAtUtc':datetime.now(timezone.utc).isoformat(),
            'aspectId':'DD-46','scope':'Starting languages, literacy, learning, scripts, translation and ordinary communication; incidental cosmology preserved without interpretation',
            'playerLanguageChapter':{'sourceFile':rel(source),'sha256':sha(source),'actualBook':rel(book),'actualBookSha256':sha(book),'paragraphs':chapter},
            'ancestryGrants':ancestry_grants,'backgroundGrants':background_grants,'runtimeLanguageAlternatives':runtime,
            'spellComparisonRecords':selected,'pendingSpellQuestionRouting':routing,'classComparisonRecords':class_records,'pendingFeatSourceComparisons':selected_feats,
            'boundedTrainingSearch':{'file':rel(source),'pattern':TRAINING.pattern,'matches':[{'line':i+1,'text':l} for i,l in enumerate(lines) if TRAINING.search(l)],'limitation':'Only this preserved Player extraction was searched; absence here is not proof that all historical sources lack a training procedure. Quick Learner is a pending source, not a current general rule.'},
            'decisionCases':[{'id':i,'title':t,'question':q} for i,t,q in CASES],
            'counts':{'sourceCases':16,'languageChapterParagraphs':24,'baseAncestries':14,'variants':sum(len(a['variants']) for a in anc['ancestries']),'backgrounds':20,'backgroundsWithLanguageField':sum(x['languageFieldPresent'] for x in background_grants),'spellComparisons':len(selected),'pendingSpellRoutes':len(routing),'classCards':sum(len(c['cards']) for c in class_records),'pendingFeatComparisons':8,'protectedFiles':len(protected)},
            'protectedFiles':protected,'sent':False,'newApprovals':0,'sourceInformationDeleted':0,'runtimeChanged':False,'cosmologyReviewed':False,
            'dispatchPrerequisite':'Capture and integrate active advanced167 and relevant earlier spell/feat decisions; refresh current interfaces before this focused conference.'}
    dump(pp,report)
    audit=A/'LANGUAGE_COMMUNICATION_SOURCE_AUDIT.md'
    text='# Languages, literacy and communication source audit — prepared, unsent\n\nThe language chapter\'s24 paragraphs match the actual Player Rulebook V6. All14 ancestry grants,45 variants and20 backgrounds are preserved, with literal source lines and complete current records. The runtime arrays remain separate evidence. This audit makes no language, spell, class or feat approval.\n\n'
    text+='The source distinctions requiring decisions include Orc/Orcish, the Troll\'s printed Giant grant versus the table\'s Trollish entry, Mycelian regional choice versus Mycelic/Sporetongue, script sharing versus comprehension, and Deep Cant versus Deep Speech. Names and population descriptions have not been converted into additional proficiency. Source prose about special tongues is receipt-only wherever its interpretation would require cosmology.\n\n'
    text+=f'The full preparation includes{len(selected)} ordinary spell comparison records,{len(routing)} routes to existing pending spell questions,{sum(len(c["cards"]) for c in class_records)} actual class cards and eight pending feat sources. Reviewed procedures retain their current authority. Quick Learner supplies a30-day pending feat text; it is not evidence of a settled universal training rule. The bounded Player-book search is recorded explicitly.\n\n'
    text+='| Case | Required decision |\n|---|---|\n'+'\n'.join(f'| {i}: {t} | {q} |' for i,t,q in CASES)+'\n\n'
    text+='[Full source preparation](LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json) contains all exact records and protected hashes. [Complete-file archive](DD_Language_Communication_Source_Prepared_v1.zip) supplies the full references. Refresh interfaces after the active advanced-crafting review before dispatch. DD-46 remains open. No deletion, push or cosmology review occurred.\n'
    audit.write_text(text,encoding='utf-8')
    files.update([pp,audit]);manifest={rel(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=rel)}
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('README_SOURCE_REVIEW.md','Prepared and UNSENT. Read LANGUAGE_COMMUNICATION_SOURCE_AUDIT.md and LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json at their listed repository paths. Decide the16 LA cases only after refreshing intervening advanced-crafting/spell/feat interfaces. Preserve every original; current spell/class approvals are comparison authority, pending feats and spells remain pending. Special-language cosmology is receipt-only until after the verified GitHub push. No exact-card promotion is requested.\n')
        z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        for p in sorted(files,key=rel):z.write(p,rel(p))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert all(hashlib.sha256(z.read(p)).hexdigest()==m['sha256'] and len(z.read(p))==m['bytes'] for p,m in manifest.items())
    assert all(sha(G/p)==h for p,h in protected.items())
    status={k:report[k] for k in ['status','preparedAtUtc','aspectId','counts','sent','newApprovals','sourceInformationDeleted','runtimeChanged','cosmologyReviewed','dispatchPrerequisite']}
    status.update(preparationFile=pp.name,preparationSha256=sha(pp),auditFile=audit.name,auditSha256=sha(audit),bundleFile=archive.name,bundleSha256=sha(archive),bundleBytes=archive.stat().st_size,payloadFiles=len(manifest),zipRoundtripVerified=True,currentFileHashes={p:m['sha256'] for p,m in manifest.items()})
    dump(A/'LANGUAGE_COMMUNICATION_SOURCE_STATUS.json',status)
    print(json.dumps({k:status[k] for k in ['status','counts','bundleFile','bundleBytes','payloadFiles','bundleSha256']}))

if __name__=='__main__':main()
