"""Preserve complete rank4-9 spell review inputs; never dispatch or approve them."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, zipfile, xml.etree.ElementTree as ET
from prepare_low_illusion_spell_source_audit import current_book_rows, digest

R=Path(__file__).resolve().parents[1]
G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.resolve().relative_to(G).as_posix()
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    out=A/'HIGHER_RANK_SPELL_FILE_HANDOFF_PREPARATION.json'
    archive=A/'DD_Higher_Rank_Spells_435_Source_Prepared_v1.zip'
    assert not out.exists() and not archive.exists(), 'Existing snapshots must be preserved'
    coverage=read(A/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json')
    low=read(A/'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json')
    low_files={x['prefix']+'_SOURCE_PREPARATION.json' for x in low['cohorts']}
    cohort_files=[f for f in coverage['cohortFiles'] if f not in low_files]
    assert len(cohort_files)==38
    cat=read(R/'data/public/spell_playtests/catalog.json')
    by={x['id']:x for x in cat['spells']}
    source=read(R/'data/playtest/spell_sources/catalog.json')
    actual=json.JSONDecoder().raw_decode((R/'src/data/spells.js').read_text(encoding='utf-8').split('export const SPELLS = ',1)[1])[0]
    core=read(R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    assert actual==source and len(by)==848
    for row in by.values():
        assert row['source']['original']==source[row['id']]
        for e in row['source']['coreEntries']+row['source']['possibleHistoricalAliases']:
            assert e['original']==core['spells'][e['index']]
    book=R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx'
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(book) as z: xml=ET.fromstring(z.read('word/document.xml'))
    paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:body/w:p',ns)]
    paragraph_indices={}
    for i,p in enumerate(paras): paragraph_indices.setdefault(p,[]).append(i)
    book_rows=current_book_rows(); book_by_line={x['line']:x for x in book_rows}
    assert len(book_rows)==936 and all(x['exactText'] in paragraph_indices for x in book_rows)
    cm=read(R/'data/public/class_playtests/manifest.json')
    class_paths={c['class']:(R/'docs/mechanics'/c['data']).resolve() for c in cm['classes']}
    deferred=set(coverage['postPushReceiptOnlyIds'])
    files=set(); historical={}; selected=[]; bindings=[]; cohorts=[]
    counterpart_count=class_count=0
    def protect(records):
        for name,h in records.items():
            assert sha(G/name)==h, ('Record a rebase before using changed historical input',name)
            historical.setdefault(name,set()).add(h); files.add(G/name)
    for f in cohort_files:
        pp=A/f; prefix=f.removesuffix('_SOURCE_PREPARATION.json'); prep=read(pp)
        sp=A/(prefix+'_SOURCE_STATUS.json'); status=read(sp); packet=A/status['packetFile']
        assert sha(packet)==status['packetSha256']
        files.update([pp,sp,packet,A/(prefix+'_SOURCE_AUDIT.md')]); protect(prep['protectedFiles'])
        assert prep['currentRankCosts']==cat['costByRank'] and prep['currentClassProgression']==cat['classProgression']
        for item in prep['selectedSpells']:
            row=item['fullSourceAndCurrentAccessRecord']
            assert row==by[item['spellId']] and item['recordSha256']==digest(row)
            assert row['operational'] is None and item['individualQuestion']
            selected.append({'spellId':item['spellId'],'questionId':item['questionId'],'preparationFile':rel(pp),
                             'recordSha256':item['recordSha256'],'minimumClassRank':min(v['rank'] for v in row['classAccess'].values()),
                             'scope':'post-push receipt only' if item['spellId'] in deferred else 'pre-push mechanics'})
        for b in prep['currentBookBindings']:
            br=b['currentBookRow']; assert br==book_by_line[br['line']]
            assert b['catalogPlacement'] in by[b['spellId']]['source']['original']['placements']
            bindings.append({**b,'actualDocxFile':rel(book),'actualDocxZeroBasedParagraphIndices':paragraph_indices[br['exactText']]})
        for other in prep['completeCounterparts']:
            assert other==by[other['id']]; counterpart_count+=1
        for c in prep['classComparisonRecords']:
            path=G/c['file'] if 'file' in c else class_paths[c['mention']['class']]
            data=read(path); files.add(path)
            if 'card' in c: assert c['card'] in data['cards']
            elif 'engine' in c: assert c['engine']==data['engine']
            else: assert c['paragraph']==data['engine'][c['engineIndex']]
            class_count+=1
        for e in prep['currentGoverningExcerpts']:
            assert sha(G/e['file'])==e['sha256']
            assert e['exactText'] in (G/e['file']).read_text(encoding='utf-8')
        cohorts.append({'prefix':prefix,'identities':len(prep['selectedSpells']),'bookBindings':len(prep['currentBookBindings']),'originalPacketSha256':sha(packet)})
    ids=[x['spellId'] for x in selected]
    pending={x['id'] for x in by.values() if x['operational'] is None and min(v['rank'] for v in x['classAccess'].values())>=4}
    assert len(ids)==len(set(ids))==435 and set(ids)==pending
    assert len(bindings)==486
    receipts=sorted(set(ids)&deferred); assert len(receipts)==47
    assert len(set(ids)|{x['spellId'] for x in low['selectedMembership']})==572
    assert sum(x['operational'] is not None for x in by.values())==276
    addenda=[]
    for f in coverage['sourceAddenda']:
        mp=A/f; jp=mp.with_suffix('.json'); d=read(jp)
        files.update([mp,jp]); protect(d.get('protectedFiles',{}))
        if 'addendumSha256' in d: assert sha(mp)==d['addendumSha256']
        if 'basePreparationSha256' in d: assert sha(A/d['basePreparation'])==d['basePreparationSha256']
        addenda.append({'file':rel(mp),'sha256':sha(mp),'evidence':rel(jp),'protectedFiles':len(d.get('protectedFiles',{}))})
    for c in cm['classes']: files.add((R/'docs/mechanics'/c['guide']).resolve())
    files.update((R/'data/playtest/class_sources').glob('*.json'))
    files.update([book,R/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',
                  G/'docs/reference/Player_Rulebook_v6_source_text.txt',R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',
                  R/'tools/prepare_low_illusion_spell_source_audit.py',R/'tools/prepare_combat_feat_source_audit.py',Path(__file__)])
    gathering=read(R/'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json')
    assert all(sha(G/p)==h for p,h in gathering['artifactHashes'].items())
    files.update(G/p for p in gathering['artifactHashes'])
    files.update([R/'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json',A/'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md',A/'GATHERING_128_EXACT_PROMOTION_RECEIPT.json'])
    files.update(R/'docs/playtest'/n for n in ['NEWCOMER_PLAYER_GUIDE.md','NEWCOMER_DIRECTOR_GUIDE.md','RESONANCE_CHEATSHEET.md'])
    files.add(A/'ONBOARDING_RULE_SUMMARY_RECONCILIATION.json')
    assert all(p.is_file() for p in files)
    report={'status':'complete higher-rank spell files prepared; UNSENT; refresh interfaces before dispatch',
            'preparedAtUtc':datetime.now(timezone.utc).isoformat(),'cohorts':cohorts,'selectedIdentities':435,
            'prePushMechanicalQuestions':388,'postPushReceiptOnlyIds':receipts,'currentBookBindings':486,
            'selectedByMinimumRank':dict(sorted(Counter(x['minimumClassRank'] for x in selected).items())),
            'actualDocxParagraphCount':len(paras),'all936BookRowsPresentInActualDocx':True,
            'originalsMatchCatalogAndCore':True,'selectedRecordsMatchCurrentCatalog':True,
            'completeCounterpartComparisons':counterpart_count,'classComparisons':class_count,
            'historicalProtectedUnion':len(historical),'historicalHashChanges':[],
            'allPendingMinimumRankFourToNineIncludedExactlyOnce':True,'combinedWithLowRankCoversAll572Pending':True,
            'ordinarySpellsOperational':276,'ordinarySpellsPending':572,'selectedMembership':selected,
            'bookBindingsWithActualDocx':bindings,'sourceAddenda':addenda,'newApprovals':0,'sent':False,
            'sourceInformationDeleted':0,'cosmologyReviewed':False,
            'dispatchPrerequisite':'Capture and integrate intervening crafting and earlier spell decisions; preserve this snapshot and create a refreshed revision. Use bounded rank/cohort conferences rather than approving an unread archive.'}
    rp=A/'HIGHER_RANK_SPELL_FILE_HANDOFF_SOURCE_CHECK.json'; assert not rp.exists(); dump(rp,report); files.add(rp)
    readme='''# Higher-rank spell complete-file preparation — UNSENT

This frozen archive supplies all435 pending ordinary spell identities with minimum current class-access rank4-9 across38 existing source cohorts. It is preparation, not an approval or a dispatched review.486 exact book placements and every selected original/Core variant/class access record are verified. All936 spell paragraphs are present in the actual supplied Player Rulebook V6.

HIGHER_RANK_SPELL_FILE_HANDOFF_SOURCE_CHECK.json maps every spell to its original focused question.388 are pre-push mechanical questions; the47 listed post-push identities are unchanged receipts only. Their incidental presence grants no cosmology review or interpretation. Combined with the separate137 low-rank identities, all572 pending spells are covered without overlap; current operational total stays276.

Read complete selected SOURCE_PREPARATION.json records and their full source files, not merely the audits. All original text packets/status records remain as historical evidence. Four source addenda retain the illusion/class, undead-profile, created-companion and metamagic comparisons. Shared names are not automatic identity or effect bindings. Complete governing rules, class guides/cards/original extracts, current spell batches, original books, gathering decisions and corrected onboarding guides are supplied. FILE_MANIFEST.json records every full payload hash and size.

Before dispatch, integrate actual advanced-crafting and intervening spell decisions, record changed interfaces, and create a fresh version without overwriting this one. Select bounded rank/cohort conferences from the exact membership map. Settle actual effects, casting, target/range/geometry, saves/attacks, duration/concentration, scaling, cost/access, ending/suppression and source conflicts; mark new operating completions NEW. Keep real world/acquisition permissions explicit. No unseen cards are approved by packaging. Final whole-game joint flow precedes the authorized GitHub push; remote verification precedes careful cosmology review.
'''
    manifest={rel(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=rel)}
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('README_SOURCE_REVIEW.md',readme.encode('utf-8'))
        z.writestr('FILE_MANIFEST.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
        for p in sorted(files,key=rel):z.write(p,rel(p))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(manifest)+2
        assert all(len(z.read(p))==m['bytes'] and hashlib.sha256(z.read(p)).hexdigest()==m['sha256'] for p,m in manifest.items())
    assert all(sha(G/p)==m['sha256'] for p,m in manifest.items())
    report.update(bundleFile=archive.name,bundleSha256=sha(archive),bundleBytes=archive.stat().st_size,payloadFiles=len(manifest),zipRoundtripVerified=True,currentFileHashes={p:m['sha256'] for p,m in manifest.items()})
    dump(out,report)
    print(json.dumps({k:report[k] for k in ['status','selectedIdentities','prePushMechanicalQuestions','currentBookBindings','historicalProtectedUnion','payloadFiles','bundleBytes','bundleSha256','sent']}))

if __name__=='__main__':main()
