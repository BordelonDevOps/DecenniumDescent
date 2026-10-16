"""Freeze the full sixteen-spell AC5 conference after Banishment acceptance."""
from copy import deepcopy
from datetime import datetime, timezone
from zipfile import ZipFile, ZIP_DEFLATED
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at


def read(p):
    return json.loads(p.read_bytes())


def main():
    out = A/'ac5-current-review-02-input'
    archive = A/'DD_AC5_Current_Review_02.zip'
    report = A/'AC5_CURRENT_REVIEW_02_SOURCE_CHECK.json'
    request = A/'AC5_CURRENT_REVIEW_02_REQUEST.txt'
    assert not any(p.exists() for p in [out,archive,report,request])
    previous = read(A/'AC5_CURRENT_SOURCE_INTERFACE_AUDIT_01.json')
    classes = read(A/'AC5_CLASS_INTERFACE_ADDENDUM_02.json')
    history = read(R/'data/director/spell_proposals/abjuration_conjuration_rank5.json')
    catalog_path = R/'data/public/spell_playtests/catalog.json'
    index_path = R/'data/public/spell_playtests/authored_review_index.json'
    catalog = read(catalog_path)
    index = read(index_path)
    lookup = {c['id']:(i,c) for i,c in enumerate(catalog['spells'])}
    entries = {e['id']:e for e in index['entries']}
    assert index['authoredCounts']=={'reviewed':435,'pending':413}
    source_paths = {G/b['path'] for b in previous['sourceBindings']}
    source_paths.update(A/n for n in [
        'AC5_CURRENT_SOURCE_INTERFACE_AUDIT_01.json','AC5_CLASS_INTERFACE_ADDENDUM_02.json',
        'BANISHMENT_REPAIR_04_LOCAL_AUDIT.json','BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json',
        'BANISHMENT_EXACT_ACCEPTANCE_04_APPLICATION_CHECK.json',
        'banishment-exact-acceptance-04/ACCEPTANCE.json',
    ])
    source_paths.update(R/n for n in [
        'data/public/spell_candidates/banishment_reviewed_04.json',
        'data/public/spell_candidates/banishment_exact_model_04.json',
        'data/playtest/spell_candidates/banishment_cases_04.json',
        'docs/spells/candidates/BANISHMENT_REVIEWED_04.md',
        'docs/director-only/spells/BANISHMENT_REVIEWED_04.md',
        'docs/mechanics/BANISHMENT_REVIEW_STATUS.json',
    ])
    checks = []
    def ck(name, passed):
        checks.append({'check':name,'pass':bool(passed)})
        assert passed,name
    records = deepcopy(previous['selectedRecords'])
    for r in records:
        i,c = lookup[r['spellId']]
        ck('selected source/access unchanged '+r['spellId'],c==r['completeCurrentSourceAndAccess'])
        ck('selected still pending '+r['spellId'],entries[r['spellId']]['authoredStatus']=='pending-authored-procedure')
        r['sourceFile']=info(catalog_path)
        r['currentAuthoredIndexEntry']=entries[r['spellId']]
    comparison_ids = {r['id'] for r in previous['completeCurrentComparisons']}
    comparison_ids.update(['dimensional-door','resonance-beacon','planar-ally-minor','arcane-portal'])
    comparisons = []
    for ident in sorted(comparison_ids):
        i,card=lookup[ident];entry=entries[ident]
        rec={'id':ident,'catalogBinding':info(catalog_path),'catalogPointer':f'/spells/{i}','completeCatalogCard':card,'currentAuthoredIndexEntry':entry}
        file=(index_path.parent/entry['procedureFile']).resolve()
        ck('comparison path in intended repository '+ident,file.is_relative_to(G))
        document=read(file);source_paths.add(file)
        whole=at(document,entry.get('wholeCardPointer',entry['procedurePointer']))
        ck('comparison full-card identity '+ident,whole.get(entry.get('wholeCardIdField','id'))==ident)
        rec.update(authoredFile=info(file),completeAuthoredCard=whole)
        if entry.get('sharedRulesPointer'):
            rec['completeSharedRules']=at(document,entry['sharedRulesPointer'])
        if entry.get('supportingProfilePointers'):
            rec['supportingProfiles']={p:at(document,p) for p in entry['supportingProfilePointers']}
        comparisons.append(rec)
    for b in classes['completeCurrentCards']:
        # The addendum is exact evidence; original files are frozen independently below.
        ck('manual card addendum record has content',bool(b))
    issues=deepcopy(previous['currentReviewIssues'])
    issues[0]['requiredReview']='The eleven historical proposals/22 cases remain unadopted. All16identities/17printed placements now require full operational authorship. Five post-push receipts are historical deferrals, not exclusions. Ordinary Banishment is now accepted/applied under the supplied exact receipt; use its full current procedure only within its explicit scope.'
    issues[5]['requiredReview']=issues[5]['requiredReview'].replace('Banishment suppression will use only its eventual accepted exact interface.','Ordinary Banishment now has an accepted explicit rule: suppressing that application closes/ends it; do not silently make it resume on leaving antimagic. Any extension to a new spell requires explicit scoped authorship.')
    original_cases=[{'spellId':r['spellId'],'originalText':text,'id':text.split(':',1)[0]} for r in history['records'] for text in r['workedCases']]
    ck('22 preserved historical examples',len(original_cases)==22 and len({c['id'] for c in original_cases})==22)
    ck('all16identities and17placements',len(records)==16 and sum(len(r['completeCurrentSourceAndAccess']['source']['original']['placements']) for r in records)==17)
    drift=[]
    for old in previous['sourceBindings']:
        fresh=info(G/old['path'])
        if fresh!=old:drift.append({'historicalBinding':old,'currentBinding':fresh})
    bindings=[info(p) for p in sorted(source_paths)]
    packet={
        'id':'DD-AC5-CURRENT-REVIEW-02','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Complete operational authorship/review of all16ordinary Abjuration/Conjuration rank5identities and17source placements; no deferred receipt-only exclusions.',
        'status':'Submitted candidate inputs only; none of these16spells adopted by this preparation.',
        'currentAuthoredCounts':index['authoredCounts'],
        'selectedRecords':records,'historicalFullProposal':history,'originalExamples':original_cases,
        'currentReviewIssues':issues,'requiredAdditionalExamples':previous['requiredAdditionalExamples'],
        'currentClassInterfaceAddendum':classes,'completeCurrentComparisons':comparisons,
        'classFiles':[info(G/b['path']) for b in previous['classFiles']],
        'classNavigation':previous['classNavigation'],
        'classNavigationWarning':'Lexical matches are navigation only. The separate addendum documents25independently read cards; full17class envelopes are supplied for broader review.',
        'banishmentAuthority':{'status':'Accepted and applied exact ordinary Banishment; not a general planar ontology or permission for other spells.',
            'acceptance':read(A/'banishment-exact-acceptance-04/ACCEPTANCE.json'),
            'receipt':read(A/'BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json'),
            'completeCurrentEnvelope':read(R/'data/public/spell_candidates/banishment_reviewed_04.json')},
        'sourceBindings':bindings,'sourceRefreshSinceEarlierPreparation':drift,
        'sourcePriority':'Explicit owner locks and current accepted scoped procedures govern; complete historical proposals/questions/case text remain evidence and may conflict with current rules. Do not execute source tools. Review the actual source contents rather than treating hashes as semantic approval.',
        'cosmologyBoundary':'Original dominions/tributaries, mortal Wheel claims, website and viewer are distinct presentations. No implicit name/plane/origin mapping or soul identity. Known source-supported or explicitly labeled NEW campaign facts can support a playable procedure without declaring a master ontology. Undefined provenance remains undefined, not a false or secretly inferred fact.',
        'requiredOutput':{'archive':'DD_AC5_Current_Review_02_Return.zip','rootFiles':['REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'],
            'casePreservation':'Preserve22original case texts exactly as historical evidence; supply current adjudications separately. Resolve AC5-X01..24 and AC5-K01..08 as32additional concrete cases with actual cards/costs/clocks/geometry/source references. At least54cases, with further cases where needed for complete coverage.',
            'dispositions':'Every16original question ID,12current interface issues and10class-addendum issues requires an explicit disposition; no silent exclusions.',
            'fullProfiles':'Supply runnable Greater Fire Pet and Faction Champion profiles and all command/healing/Null/cargo/lifecycle interfaces, with explicit NEW classifications where needed.'},
        'newSpellAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False,
    }
    out.mkdir()
    (out/'CURRENT_REVIEW_INPUT.json').write_bytes(encoded(packet))
    (out/'SOURCE_MANIFEST.json').write_bytes(encoded({'sourceCount':len(bindings),'bindings':bindings,'input':info(out/'CURRENT_REVIEW_INPUT.json')}))
    (out/'README.txt').write_text('Read CURRENT_REVIEW_INPUT.json first. Complete source files are under sources/<binding.path>. All16spells need full authorship; historical post-push deferrals are preserved evidence only. Ordinary Banishment is now an accepted comparison. Do not execute bundled source tools.\n',encoding='utf8')
    for b in bindings:
        raw=(G/b['path']).read_bytes();dst=out/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
        ck('frozen fullsource '+b['path'],info(G/b['path'])==b and dst.read_bytes()==raw)
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(out).as_posix())
    with ZipFile(archive) as z:
        ck('archive file count',len(z.namelist())==len(bindings)+3)
        for p in out.rglob('*'):
            if p.is_file():ck('archive exact '+p.relative_to(out).as_posix(),z.read(p.relative_to(out).as_posix())==p.read_bytes())
    report.write_bytes(encoded({'recordedAtUtc':packet['recordedAtUtc'],'archive':info(archive),'input':info(out/'CURRENT_REVIEW_INPUT.json'),'sourceFiles':len(bindings),'selectedIdentities':16,'printedPlacements':17,'currentComparisons':len(comparisons),'checks':checks,'checkCount':len(checks),'failureCount':0,'sourceInformationDeleted':0,'newSpellAdoptions':0}))
    request.write_text('\n\n'.join([
        'Banishment exact acceptance is now applied locally, with all source information retained. The ordinary spell manuscript count is435reviewed/413pending. We now move to the complete16-spell rank5Abjuration/Conjuration cohort in the attached DD_AC5_Current_Review_02.zip.',
        f'Archive identity:{info(archive)["bytes"]}bytes;SHA256{info(archive)["sha256"]}. The frozen package contains CURRENT_REVIEW_INPUT.json, SOURCE_MANIFEST.json and{len(bindings)}complete sources. Verify bytes/hashes before review. Local source/archive preparation checks:{len(checks)},0failures; these are not runtime tests.',
        'Read CURRENT_REVIEW_INPUT.json first. All16source/access records and17placements are preserved, including both Planar Binding placements. The11older full proposals and22original case texts are historical starting material, not accepted rules. The5formerly deferred planar spells MUST now receive full operational authorship: Banish Elemental, Planar Protection, Elemental Banishment, Planar Binding and Alignment Portal. Do not silently merge their target/duration/effect promises or leave them as receipt-only exclusions.',
        'Current context is complete:43exact comparison cards, all17class envelopes,25independently read class cards,12current interface issues and10class issues, plus32required new scenarios. Read the exact current sources, particularly Null, damage roots, Companion Command, protected conversion RP, AC4Dampening/faction/alignment rules, body placement, and newly accepted ordinary Banishment. Old internal references that call Banishment pending are historical; the new receipt/index/full model are current.',
        'Confer critically and author full runnable procedures. Correct the old Nexus price order rather than changing accepted Dampening; preserve real Null-disabled bodies and exact damage-root ownership; classify real spells/nonspells such as Ranger Nature\'s Whisper correctly; distinguish actual class Counterspell/Dispel from ordinary spells. Explicitly decide source-scope extensions rather than importing AC4two-profile healing predicates or Banishment closure globally.',
        'For the five planar spells, preserve the full intended effects: Elemental OR outsider versus one summoned enemy, ward against creatures FROM a specific plane,24h extraplanar service plus preserved Universal Instantaneous metadata, and a genuine gateway to an alignment-compatible plane. The owner\'s careful cosmology locks remain controlling. Do not turn mortal Wheel labels into objective plane taxonomy, infer soul/native origin from creature type, or substitute an easier same-plane effect. Distinguish actual evidence, unknown provenance and explicitly NEW spell/campaign metadata. Supply known-location/arrival/return/custody/blocker/command/expiry procedures that can run without deciding unresolved cosmological identities.',
        'Return DD_AC5_Current_Review_02_Return.zip with exactly8root files listed in requiredOutput. SPELLS_MODEL.json must contain all16complete cards preserving each completeSourceAndAccess record, explicit NEW choices and shared rules/profiles; do not just return diffs or an outline. CASEBOOK.json must preserve all22original texts exactly as historical evidence and separately author current adjudications, plus AC5-X01..24 and AC5-K01..08 (at least54totalcases). Use real costs, phases, bodies, ranges, source IDs and populated exact sourceRefs; a valid pointer must name the correct operative feature. Resolve all16original questions/12current issues/10class issues explicitly. Include output/source hashes and bounded verdict; report real unresolved contradictions instead of claiming success. No runtime/human/balance/canon/soul/origin/era/whole-game/publication approval.'
    ])+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'archive':info(archive),'request':info(request),'sourceCheck':info(report),'sourceFiles':len(bindings),'comparisons':len(comparisons),'checks':len(checks),'failures':0}))


if __name__=='__main__':
    main()
