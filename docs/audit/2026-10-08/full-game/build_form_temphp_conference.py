"""Consolidate exact source roles for the next form/buffer conference."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
base=json.loads((HERE/'FORM_TEMP_HP_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
sup=json.loads((HERE/'FORM_TEMP_HP_SUPPLEMENTAL_SOURCES.json').read_text(encoding='utf-8'))
spells=json.loads((HERE/'FORM_TEMP_HP_SPELL_SOURCES.json').read_text(encoding='utf-8'))
semantic=json.loads((HERE/'FORM_TEMP_HP_SEMANTIC_SOURCES.json').read_text(encoding='utf-8'))
records=[]
for r in base['classRecords']+semantic['classRecords']+sup['bardRecords']:
 r=dict(r)
 r['bindingId']=r['card']['id'] if r['kind']!='class-engine' else f"{r['owner']}.engine[{r['engineIndex']}]"
 records.append(r)
for r in sup['featRecords']+spells['spellRecords']+semantic['spellRecords']:
 r=dict(r);r['bindingId']=r['kind']+':'+r['sourceId'];records.append(r)
for r in semantic['v6Records']:
 if r['prefix']=='Temporary Hit Points':continue
 r=dict(r);r['bindingId']='v6-trait:'+r['prefix'].strip('.').lower().replace(' ','-');records.append(r)
supports=sup['supportingSources']+semantic['coreSupports']+[r for r in semantic['v6Records'] if r['prefix']=='Temporary Hit Points']
assert len(records)==len({r['bindingId'] for r in records})==175 and len(supports)==5
data={'status':'UNREVIEWED:175 candidate roles+5 supports, conference prepared but not submitted',
      'scope':'Full Druid66 passages;64 other initial class/Bard passages;26 semantic class cards;7 feats;9 ordinary spells;3 recovered V6 ancestry traits. Individual form/buffer/guard/previous/deferred classification required. Not whole-catalog completeness.',
      'records':records,'supportingSources':supports,'druidMetadata':semantic['druidMetadata'],
      'druidMetadataSha256':semantic['druidMetadataSha256']}
(HERE/'FORM_TEMP_HP_CONFERENCE_SOURCES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
questions=(HERE/'FORM_TEMP_HP_REVIEW_QUESTIONS.md').read_text(encoding='utf-8')
questions=questions[questions.index('## Buffer identity'):]
lines=['# Form and temporary-HP source conference','',
 'Codex → Calibration Review. Next exact corpus:175 source-role records+5 supporting passages. The user wants every aspect developed and discussed, preserving existing named content. This packet is UNREVIEWED and no full effects are presumed complete. Please classify all175 exact IDs once (grouping IDs is fine; no ambiguous abbreviation), reconcile the questions below, and specify implementable bounded decisions. Distinguish existing rules, NEW source gap-fills, and genuine remaining dependencies. Do not add named powers or import another edition. All original files remain preserved.',
 '',data['scope'],'',questions,
 '', '## Additional recovered evidence and semantic questions',
 '16. V6 explicitly supplies the default temporary-HP expiry: until depleted or after a long rest, unless specified otherwise. Core recovered this as compatible. Resolve grant ties and source-specific expiry without giving an overwritten shield a hidden reserve. Clarify whether a long rest ends source-specific longer-duration grants or only unspecified-duration grants; use the exact precedence.',
 '17. V6 ancestry Consume Decay, Battle Cry and Soul Drain were omitted by name-only race registries. Their exact mechanical passages are included. Classify their buffer amount/duration/payment/event integration without pretending the ancestry catalog is complete. Soul Drain temporary HP must use actual resolved damage and cannot farm created/friendly/trivial/repeated bodies under agreed resource guards. If a specific anti-farm restriction is a NEW global extension, label it.',
 '18. Non-Druid transformation/natural-attack/cosmetic/perception cards are included as semantic supplements. Classify which actually alter anatomy/statistics or need form-state contracts, versus named defense/control effects or existing appearance-only rules. Do not turn every ability called Form into Druid Shapeshifting or transfer Buffer Reserve across classes. Preserve Mage lich physiology, Oracle intrinsic Curse and Spirit Walk one-character/two-positions damage identity, Warrior mutation concurrency and existing Strain/resource guards.',
 '19. Shapechange, Polymorph, True Polymorph and Mass Polymorph have unfinished original spell entries. Classify explicit dependencies on the bounded form/stat/body model and propose a coherent route to completing these EXISTING named spells. Do not authorize importing unlimited monster stat blocks or make them operational by name alone. Exact operational spell profiles can be the follow-up spell batch after buffer/form chassis.',
 '20. Full Druid metadata and current worked example are included beyond66 engine/card passages. Preserve detailed shift progression, Base/Arch/Hero stage exceptions, Circle gates, level11 two-form attunement, legal prepared spells and protected Refrain behavior. Resolve early voluntary reversion cost versus a paid change; unchanged-form renewal; returning to a former form and once-transformation Surge uses; anatomy-compatible equipment bonuses; fall consequences when flight ends; no HP reroll or independent body.',
 '', '## Five exact supporting passages',json.dumps(supports,ensure_ascii=False,indent=2),
 '', '## Druid metadata',json.dumps(semantic['druidMetadata'],ensure_ascii=False,indent=2)]
for r in records:
 lines+=['','## '+r['bindingId']]
 if r['kind']=='class-engine':lines+=[r['text'],'SHA256 '+r['textSha256']]
 elif r['kind'] in ('class-card','bard-card'):
  c=r['card'];lines+=[json.dumps(c,ensure_ascii=False,separators=(',',':')),'SHA256 '+r['sourceObjectSha256']]
 elif r['kind']=='ordinary-spell':
  lines+=['Original: '+json.dumps(r['sourceObject'],ensure_ascii=False,separators=(',',':')),
          'Current overlay: '+json.dumps(r['overlayObject'],ensure_ascii=False,separators=(',',':'))]
 elif r['kind']=='feat':lines+=[json.dumps(r['sourceObject'],ensure_ascii=False,separators=(',',':')),'SHA256 '+r['sourceObjectSha256']]
 else:lines+=[r['text'],'V6 line '+str(r['line'])+' SHA256 '+r['textSha256']]
out=HERE/'CODEX_FORM_TEMP_HP_CONFERENCE_PREPARED.md';out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Prepared175+5 conference, {out.stat().st_size} bytes. Not yet submitted.')
