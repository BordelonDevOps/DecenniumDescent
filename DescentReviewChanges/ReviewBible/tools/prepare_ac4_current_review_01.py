"""Freeze the next fifteen complete spell proposals with current authoritative interfaces."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()
def pointer(value,path):
    for part in path.lstrip('/').split('/') if path else []:
        part=part.replace('~1','/').replace('~0','~');value=value[int(part)] if isinstance(value,list) else value[part]
    return value

def main():
    root=A/'ac4-current-review-01-input';archive=A/'DD_AC4_Current_Review_01.zip';receipt=A/'AC4_CURRENT_REVIEW_01_PREPARATION.json'
    assert not any(p.exists() for p in [root,archive,receipt])
    proposal_path=R/'data/director/spell_proposals/abjuration_conjuration_rank4.json';old=read(proposal_path)
    base=R/'data/public/spell_playtests';catalog=read(base/'catalog.json');index=read(base/'authored_review_index.json')
    by={x['id']:x for x in catalog['spells']};ix={x['id']:x for x in index['entries']};paths=set();cache={}
    def include(p):
        p=Path(p).resolve();assert p.is_file() and p.is_relative_to(G.resolve()),str(p);paths.add(p);return p
    def load(p):
        p=include(p)
        if p not in cache:cache[p]=read(p)
        return cache[p]
    for name in old['sourceFiles']:include(G/name)
    preparation=load(A/'ABJURATION_CONJURATION_RANK4_SOURCE_PREPARATION.json')
    include(R/'data/playtest/spell_sources/catalog.json')
    for name in ['data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json','src/data/spells.js','rulebook_output.txt','class_spell_school_mapping.csv','class_spell_progression.csv','data/public/class_playtests/manifest.json','docs/mechanics/CLASS_PLAYTEST_RULES.md','docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md','docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md','docs/mechanics/CLASS_COMBINED_ENGINE_PLAYTEST.md']:
        p=R/name
        if p.exists():include(p)
        else:assert name=='docs/mechanics/CLASS_COMBINED_ENGINE_PLAYTEST.md',name
    for p in [proposal_path,R/'docs/spells/proposals/ABJURATION_CONJURATION_RANK4.md',base/'authored_review_index.json',base/'catalog.json',base/'candidate_low_rank_136.json',A/'CURRENT_SPELL_REVIEW_RECONCILIATION_01.json',Path(__file__)]:include(p)
    current_counterparts=[]
    counterpart_ids=[x['id'] for x in old['completeCurrentCounterparts']]+['alignment-purge','faction-omniscience','resonance-sight-supreme']
    for ident in counterpart_ids:
        e=ix[ident];p=(base/e['procedureFile']).resolve();container=load(p)
        row={'id':ident,'currentAuthoredIndexEntry':e,'file':info(p),'wholeCardPointer':e['wholeCardPointer'],'wholeCard':pointer(container,e['wholeCardPointer'])}
        if e.get('sharedRulesPointer'):row['sharedRules']=pointer(container,e['sharedRulesPointer'])
        for field in ['authoredAcceptanceReceipt','completeEnvelopeBinding']:
            if field in e:include(G/e[field]['path'])
        current_counterparts.append(row)
    class_manifest=load(R/'data/public/class_playtests/manifest.json');classes=[];class_matches=[]
    terms=['reflect','spell shield','counterspell','null','alignment','faction','teleport','summon','companion','discount','resonance','purge']
    for row in class_manifest['classes']:
        path=(R/'docs/mechanics'/row['data']).resolve();full=load(path);classes.append({'class':row['class'],'file':info(path),'completeEnvelopeSupplied':True})
        for i,card in enumerate(full['cards']):
            matching=[t for t in terms if t in json.dumps(card,ensure_ascii=False).lower()]
            if matching:class_matches.append({'class':row['class'],'file':info(path),'jsonPointer':f'/cards/{i}','id':card['id'],'name':card['name'],'matchingTerms':matching})
    assert len(classes)==17
    new_sources=[
      'docs/mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md','docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md','docs/mechanics/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_PLAYTEST.md',
      'docs/director-only/cosmology/PLANES_REVIEWED_01.md','docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md',
      'data/director/cosmology/epilogue_character_reviewed_01.json','data/director/cosmology/epilogue_relic_null_reviewed_01.json','data/director/cosmology/epilogue_campaign_arcs_reviewed_01.json',
      'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md','docs/mechanics/expedition/EXPEDITION_DIRECTOR_BOOK.md','docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json',
      'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md','docs/spells/candidates/DI7_SHAMAN_CASTING_INTERFACE.md']
    for name in new_sources:include(R/name)
    for name in ['DI7_EXACT_ACCEPTANCE_RECEIPT.json','di7-exact-final-verdict/DI7_EXACT_ACCEPTANCE_AUTHORITY.json','COSMOLOGY_EPILOGUE_RELIC_NULL_01_APPLICATION_CHECK.json','COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_APPLICATION_CHECK.json']:include(A/name)
    core=load(R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json');literal=load(R/'data/playtest/spell_sources/catalog.json')
    records=deepcopy(old['records']);checks=[]
    def ck(name,ok):checks.append({'name':name,'passed':bool(ok)});assert ok,name
    ck('15 unique complete proposals',len(records)==len({x['spellId'] for x in records})==15)
    ck('Current authored counts',index['authoredCounts']=={'reviewed':419,'pending':429})
    for record in records:
        ident=record['spellId'];card=by[ident]
        ck(ident+' preserved complete source/access',record['fullSourceAndCurrentAccessRecord']==card)
        ck(ident+' remains unreviewed',ix[ident]['authoredStatus']=='pending-authored-procedure' and ix[ident]['procedurePointer'] is None)
        ck(ident+' original catalog',card['source']['original']==literal[ident])
        for ent in card['source']['coreEntries']+card['source']['possibleHistoricalAliases']:ck(ident+' Core '+str(ent['index']),ent['original']==core['spells'][ent['index']])
        record['currentIndexEntry']=deepcopy(ix[ident]);record['status']='Complete proposal in dedicated current-interface review; not adopted.'
    raw_book=(R/'rulebook_output.txt').read_bytes()
    book_encoding='utf-16' if raw_book.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'
    lines=raw_book.decode(book_encoding).splitlines()
    for binding in old['originalBookBindings']:
        row=binding['currentBookRow'];ck('Book line '+str(row['line']),lines[row['line']-1].strip()==row['exactText'].strip())
    # Preserve every earlier example with a stable review ID.
    examples=[{'id':record['questionId']+'-'+chr(65+i),'spellId':record['spellId'],'originalText':text,'evidenceKind':'authored example, not runtime test'} for record in records for i,text in enumerate(record['workedCases'])]
    ck('30 original examples',len(examples)==len({x['id'] for x in examples})==30)
    questions=[
      ('AC4-R01','Reflection and transfer identity','The old shared arbitration sentence treats all copies/reflections as preserving a causal root. The current Null rules distinguish pure transfer/redirection from an explicitly new reflected/retaliatory damage root. Spell Shield currently proposes redirecting the single original payload before attack/save, retaining original caster ownership/stats/concentration. Independently decide this exact mechanism and record cast identity, damage dealer/root creation, Null flag, return targeting, ongoing target branch, concentration, source rank and no-copy/recursive-reflection limits. Do not grant universal root semantics to other reflection sources.'),
      ('AC4-R02','Alignment Lock/Anchor against current Purge and Suggestion','The seven DI7 cards are now reviewed, including the named AP-AS-01 exception. It is not a universal priority taxonomy. Define this new lock family’s exact interaction with Purge and Suggestion in both cast orders, underlying changes, suppression and zone exit/reentry; no fabricated undefined axes or cast-order staircase. Preserve both Alignment Anchor placements and the rank7 conduct clause with its bounded hard-denial guard. Any additional exception must be explicit NEW authorship, not attributed to old accepted text.'),
      ('AC4-R03','Faction history and actual permissions','The expedition/reputation review is now complete within its own authored scope; the old statement that it is pending is historical. Use the actual preserved standing policy/version and independently established membership/affiliation/invocation records. Do not invent permissions or treat favorable standing, null fields, a temporary summoned affiliation or DI7 information access as membership.'),
      ('AC4-R04','Finite summons and Null zero','Water Pet and Faction Envoy need the current Null Disabled override for qualifying damage at0; independent expiry, replacement, dismissal and concentration ending still end their bodies. Separate source owner from controller, source type from humanoid appearance, no-resource lifecycle and actual gear custody. Decide whether Water Pet healing deliberately spends the offensive allowance as a scoped NEW exception; ordinary pure support only spends the shared command. Supply complete profiles and control timing, not nominal CR alone.'),
      ('AC4-R05','Legal casting and the new RP surcharge','Review Dampening Field’s proposed new RP-price interface for otherwise charge-only/free spells explicitly, including no-pool actors, waivers, class reductions/minimums, mandatory extras, Dissonance/Refrain and final Influence. This is proposed NEW behavior, not already established by Influence. Preserve all class access, current caster engine and item-source requirements; a nonspell technique or Oracle RC feature is not automatically a spell.'),
      ('AC4-R06','Timing, invalid eligibility and suppression','Resolve exact endpoints for every one-minute/ten-minute/24-hour/seven-day procedure and the distinct two-turn Bind Element. Keep fixed virtual markers or absolute deadlines as the chosen source requires; no restart through extra turns, initiative reorder or absence. Distinguish known illegal choices from hidden eligibility; do not reveal alignment, faction, type or obstruction through free validation. Fully specify suppressed bodies, conditions and occupied return geometry.'),
      ('AC4-R07','Source conflicts and full effect fidelity','Explicitly disposition Spell Shield’s level3/Tier3 language and Elemental Drain’s catalog2RP/Core5RP conflict. Retain both originals. Check every printed effect/placement, geometry, save, lifetime, current HP/life consequence, cost and rejection path for all15 cards; no global rank collapse, missing effect or shortcut to achieve acceptance.'),
      ('AC4-R08','Spatial and local-module integrations','Check Dimensional Anchor endpoints/atomic group travel versus Dimensional Door and Beacon; Corruption Barrier forced crossing/carried bodies/falling; opaque Crystalline Barrier whole40HP and support. Apply the exact current Xi spell-target branch and Null rules without turning bounded epilogue machines into universal spells. Accepted campaign arcs do not grant generic climate, planar or soul authority.'),
      ('AC4-R09','Banishment historical sequencing hold','The owner-authorized progress push and careful cosmology review have occurred. Banishment is still a source-only receipt because no complete procedure has yet been authored, not because the push is pending. Preserve its full receipt and original source; do not count it among these15 or silently approve it. It remains a separate next-authoring obligation using the current planes/souls sources, with no erased identity or permanent procedural block.')]
    cases=[
      ('AC4-X01','Spell Shield: original Veiled caster, un-Veiled recipient, return to original caster; record exact dealer/root and life outcome.'),
      ('AC4-X02','Spell Shield: Veiled reflector and un-Veiled original caster; contrast the adopted redirect or new-damage mechanism and preserve real concentration.'),
      ('AC4-X03','Lock then Purge then new Suggestion from a different caster; state every effective/underlying axis through each ending, including no-ratcheting.'),
      ('AC4-X04','Purge then Lock, zone exit and reentry, overlapping locks and an undefined-axis creature; retain real costs/deadlines.'),
      ('AC4-X05','A temporary faction-affiliated Envoy approaches member-only Sanctuary while its owner has valid membership; do not manufacture Envoy membership.'),
      ('AC4-X06','Qualifying Null damage reduces a Water Pet to0 before its spell expiry; apply disabled state, a legal heal if any and subsequent independent expiry.'),
      ('AC4-X07','One owner commands a Water Pet heal and another companion attack in the same numbered round; resolve shared command and any explicit scoped support/offense exception.'),
      ('AC4-X08','Dampening Field plus final Ease, a waived RP-priced cast, a charge-only spell, an actor with no RP pool and an actual nonspell RC feature.'),
      ('AC4-X09','Anchor appears after an atomic group travel commitment; resolve all bodies and cargo once, keep costs, and compare two outside endpoints whose imagined path crosses the sphere.'),
      ('AC4-X10','Corrupted carried passenger contacts the barrier, an unsupported fall crosses it and an unrelated traveler teleports beyond it; finite contact clocks and actual damage.'),
      ('AC4-X11','Bind Element versus exact type eligibility, a previously spent hard guard, suppression and a second-turn boundary; no new free application.'),
      ('AC4-X12','Crystalline Barrier loses HP, is suppressed while a body occupies its footprint, and reaches original expiry before clearing; no renewed body or stock.'),
      ('AC4-X13','Greater Warding on a Warding Bond recipient: spell-origin11damage, resistance, conserved split, tempHP and concentration with no second mitigation.'),
      ('AC4-X14','Elemental Drain on an active creature-classified Undead with an actual RP pool, on a true dead body and on a damage-immune eligible target; clarify actual living/active predicates rather than infer from names.'),
      ('AC4-X15','Beacon source support moves or is destroyed after traveler commitment; reject duplication/free retry and compare Xi ending one eligible ongoing target branch.')]
    source_drift=[{'path':name,'historical':value,'current':info(G/name)} for name,value in old['sourceFiles'].items() if info(G/name)['sha256']!=value['sha256']]
    source_bindings=[info(p) for p in sorted(paths)]
    payload={'id':'AC4-CURRENT-REVIEW-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Prepared dedicated review; not submitted or adopted at creation.',
      'scope':'All15 complete minimum-rank4 Abjuration/Conjuration proposals, including both rank4/rank7 Alignment Anchor placements. Banishment remains a separately recorded source-only authoring obligation.',
      'historicalProposal':info(proposal_path),'records':records,'historicalSharedProposalPreserved':old['sharedProposal'],'sharedProposalStatus':'Earlier proposal supplied intact for explicit correction under AC4-R01..09; current accepted interfaces below control their own scope.',
      'currentCounterparts':current_counterparts,'currentClasses':classes,'nonExhaustiveClassCardNavigation':class_matches,
      'classNavigationWarning':'Keyword pointers are navigation aids, not proof of exhaustive semantic coverage. All17 complete actual class envelopes are supplied; use actual source engine/card scope.',
      'currentGoverningDocuments':[info(G/name) for name in old['currentGoverningDocuments']],'newCurrentInterfaces':[info(R/name) for name in new_sources],
      'newFactionAllyProfile':old['newFactionAllyProfile'],'publicCr3ComparisonRecords':old['publicCr3ComparisonRecords'],
      'originalBookBindings':old['originalBookBindings'],'preservedCatalogCoreConflicts':old['preservedCatalogCoreConflicts'],'banishmentSourceOnlyReceipt':old['postPushReceipts'],
      'sequencingHoldUpdate':'The prior pre-push sequencing restriction is satisfied. This batch completes15 already prepared proposals; Banishment still needs its separate complete authored procedure, not another push.',
      'currentAuthoredCounts':index['authoredCounts'],'originalExamples':examples,'currentInterfaceQuestions':[{'id':i,'title':t,'question':q} for i,t,q in questions],
      'requestedIntegrationExamples':[{'id':i,'scenario':s,'expectedOutcome':'To be fully authored and independently reviewed; no executed test claimed.'} for i,s in cases],
      'historicalSourceDrift':source_drift,'sourceBindings':source_bindings,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False,'newRulesAdopted':False}
    # No input, existing candidate, public catalog or count is changed.
    for p,binding in zip(sorted(paths),source_bindings):ck('Input unchanged '+binding['path'],info(p)==binding)
    root.mkdir();(root/'CURRENT_REVIEW_INPUT.json').write_bytes(encoded(payload));(root/'SOURCE_BINDINGS.json').write_bytes(encoded(source_bindings))
    request='Review all15 complete spell proposals in CURRENT_REVIEW_INPUT.json using the full current sources under sources/. Preserve all current access/source/placement records and all30 original example IDs. Independently disposition every original AC4 question and AC4-R01..09. Complete all15 requested integration examples with concrete results, not mere test specifications. Resolve needed new bounded mechanics explicitly, keeping accepted source scopes intact. Return DD_AC4_Current_Review_01_Return.zip with exactly REGISTER.json, SPELLS_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_REVIEW.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json at root. Supply complete readable15-card procedures, full source/access evidence and both Alignment Anchor placements. Preserve Banishment as the separate source-only authoring obligation, with its obsolete pre-push sequencing hold explicitly distinguished. Give exact archive bytes/SHA256 and a full-module verdict or precise remaining corrections. No canon, runtime, balance, human or whole-game approval is requested.\n'
    (root/'README_REVIEW.txt').write_text(request,encoding='utf8',newline='\n')
    (root/'LOCAL_SOURCE_CHECK.json').write_bytes(encoded({'checks':checks,'checkCount':len(checks),'failureCount':0,'sourceFiles':len(paths),'originalExamples':30,'proposedCards':15,'interfaceQuestions':9,'requestedNewExamples':15,'sourceIntegrityOnly':True,'runtimeTestsExecuted':0}))
    with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.iterdir()):z.write(p,p.name)
        for p in sorted(paths):z.write(p,'sources/'+p.relative_to(G).as_posix())
    with ZipFile(archive) as z:
        for binding in source_bindings:
            raw=z.read('sources/'+binding['path']);assert len(raw)==binding['bytes'] and digest(raw)==binding['sha256']
    receipt.write_bytes(encoded({'recordedAtUtc':payload['recordedAtUtc'],'archive':info(archive),'reviewInput':info(root/'CURRENT_REVIEW_INPUT.json'),'sourceBindings':info(root/'SOURCE_BINDINGS.json'),'check':info(root/'LOCAL_SOURCE_CHECK.json'),'sourceFiles':len(paths),'sourceChecks':len(checks),'failureCount':0,'cards':15,'originalExamples':30,'requestedIntegrationExamples':15,'currentInterfaceQuestions':9,'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'submitted':False,'historicalSourceDrift':source_drift}))
    print(json.dumps({'archive':info(archive),'receipt':info(receipt),'sourceFiles':len(paths),'checks':len(checks),'failures':0,'classNavigationRecords':len(class_matches)}))

if __name__=='__main__':main()
