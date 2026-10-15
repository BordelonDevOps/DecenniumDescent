"""Preserve a post-push source/authority packet without changing setting doctrine."""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import hashlib, json, re, subprocess, zipfile
import xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded

BASE = 'a3f75a0ce577f51bd39153a872ef05ba9e877642'
D = Path('C:/Users/cbord/Documents/ChatGPT/Decennium Descent/github-delivery')

def read(p): return json.loads(p.read_bytes())
def sha(raw): return hashlib.sha256(raw).hexdigest()
def git(*args): return subprocess.run(['git', '-c', 'core.longpaths=true', *args], cwd=D, capture_output=True, check=True).stdout

def main():
    work = A / 'cosmology-source-authority-01'
    archive = A / 'DD_Cosmology_Source_Authority_01.zip'
    receipt = A / 'COSMOLOGY_SOURCE_AUTHORITY_01_PREPARATION.json'
    assert all(not p.exists() for p in [work, archive, receipt])
    assert git('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == BASE
    tree = {}
    for record in git('ls-tree', '-r', '-z', BASE).split(b'\0'):
        if not record: continue
        meta, name = record.split(b'\t', 1); mode, kind, oid = meta.decode().split()
        if kind == 'blob': tree[name.decode('utf-8')] = oid
    base_paths = [
        ('docs/canon/CANON_MANIFEST.json', 'domain-registry'),
        ('docs/canon/REPOSITORY_PROMOTION.md', 'promotion-policy'),
        ('docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md', 'recorded-owner-directions'),
        ('docs/mechanics/SILENT_ONES_CANON.md', 'recorded-owner-directions-and-interpretation'),
        ('docs/mechanics/APPENDIX_B_FOLK_RELIGION.md', 'folk-religion-treatment-and-patch-history'),
        ('docs/mechanics/PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md', 'historical-publication-patch-report'),
        ('docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md', 'registered-director-endgame-source'),
        ('docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md', 'registered-override-tracker'),
        ('docs/playtest/MATRIX_OF_OBLIVION_EXTRACT.md', 'matrix-extract-and-continuity-notes'),
        ('docs/playtest/DUNGEON_CREATION_PURPOSE.md', 'origin-synthesis-with-owner-lock-notes'),
        ('docs/manuals/CONTINUITY_B_COSMOLOGY.md', 'historical-continuity-audit'),
        ('docs/manuals/DIRECTOR_MATERIALS_VISIBILITY.md', 'publication-boundary'),
        ('src/data/cosmology-lore.json', 'existing-runtime-data'),
        ('src/components/CosmologyViewer.tsx', 'existing-runtime-consumer'),
        ('src/app/page.tsx', 'existing-runtime-entrypoint'),
    ]
    sources = list(base_paths)
    for name, kind in base_paths:
        if (R/name).is_file(): sources.append(((R/name).relative_to(G).as_posix(), kind + '-review-build-counterpart'))
    sources += [
        ('The Cosmology of Decennium Descent.docx', 'original-root-source-document-status-to-reconcile'),
        ('The Decennium Descent and the Matrix of Oblivion.docx', 'original-root-source-document-status-to-reconcile'),
        ('The_World_of_Aethel_Lore.docx', 'original-root-source-document-status-to-reconcile'),
        ('The_Cosmology_of_Decennium_Descent_EXTRACT.txt', 'existing-derived-text-extract'),
        ('DescentReviewChanges/ReviewBible/docs/canon/CANON_CORE.md', 'review-build-setting-synthesis'),
        ('DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md', 'review-build-publication-boundary'),
        ('DescentReviewChanges/ReviewBible/docs/director-only/continuity/SILENT_ONES_CANON.md', 'director-labeled-preserved-counterpart'),
        ('DescentReviewChanges/ReviewBible/docs/director-only/runtime-source/cosmology-lore-unfiltered.json', 'director-labeled-preserved-counterpart'),
    ]
    assert len({p for p, _ in sources}) == len(sources)
    inventory = []; paragraphs = {}; docs = {}; by_hash = defaultdict(list)
    for name, category in sources:
        p = G/name; assert p.is_file(), name
        raw = p.read_bytes(); git_oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert tree.get(name) == git_oid, ('Source diverged from verified delivered baseline', name)
        row = {**info(p), 'inventoryCategory': category, 'baselineGitBlob': git_oid, 'matchesDeliveredCommit': True}
        by_hash[row['sha256']].append(name)
        if p.suffix == '.docx':
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            entries = []
            with zipfile.ZipFile(p) as z:
                text_parts = sorted(n for n in z.namelist() if re.fullmatch(r'word/(?:document|footnotes|endnotes|comments|header\d+|footer\d+)\.xml', n))
                for part in text_parts:
                    root = ET.fromstring(z.read(part))
                    for i, para in enumerate(root.findall('.//w:p', ns)):
                        text = ''.join(t.text or '' for t in para.findall('.//w:t', ns))
                        entries.append({'part': part, 'paragraphIndexZeroBased': i, 'text': text, 'textSha256': sha(text.encode())})
                row['textPartsIndexed'] = text_parts
                row['mediaAndEmbeddingParts'] = [n for n in z.namelist() if n.startswith(('word/media/', 'word/embeddings/'))]
            row['indexedParagraphs'] = len(entries)
            row['indexedTextCharacters'] = sum(len(x['text']) for x in entries)
            row['extractionLimits'] = 'Text-run transcription with original XML part/paragraph positions; no rendered layout, illustration or exhaustive semantic review claimed. Full DOCX bytes preserved in packet.'
            paragraphs[name] = entries
        elif p.suffix == '.json':
            docs[name] = json.loads(raw)
        else:
            text = raw.decode('utf-8-sig'); docs[name] = text
        inventory.append(row)
    registries = ['docs/canon/CANON_MANIFEST.json', 'DescentReviewChanges/ReviewBible/docs/canon/CANON_MANIFEST.json']
    domain_lists = {n: [d['domain'] for d in docs[n]['domains']] for n in registries}
    assert all(not any('cosmolog' in domain for domain in domains) for domains in domain_lists.values())
    runtime_paths = ['src/data/cosmology-lore.json', 'DescentReviewChanges/ReviewBible/src/data/cosmology-lore.json', 'DescentReviewChanges/ReviewBible/docs/director-only/runtime-source/cosmology-lore-unfiltered.json']
    assert len({info(G/n)['sha256'] for n in runtime_paths}) == 1
    world = 'The_World_of_Aethel_Lore.docx'
    placeholders = [x for x in paragraphs[world] if '[...Existing Sections I–VI remain unchanged...]' in x['text']]
    assert len(placeholders) == 1
    def lines(name, needle):
        text = docs[name]; assert isinstance(text, str)
        found = [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1) if needle in line]
        assert found, (name, needle)
        return {'path': name, 'matchingLines': found}
    owner = 'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md'
    folk = 'docs/mechanics/APPENDIX_B_FOLK_RELIGION.md'
    viewer = 'src/components/CosmologyViewer.tsx'
    findings = [
        {'id': 'COS-A01', 'kind': 'authority-registration-gap', 'evidence': {'registryDomains': domain_lists},
         'finding': 'Neither registry has a dedicated general cosmology domain. Registered locked-baselines and floor-97-old-god-endgame have narrower authorities; root placement is not automatic promotion.',
         'next': 'Confer over domain authority and existing owner locks before assigning a general cosmology owner. No authority is created by this inventory.'},
        {'id': 'COS-A02', 'kind': 'source-completeness-gap', 'evidence': {'path': world, 'paragraphs': placeholders},
         'finding': 'This world-lore document explicitly retains a placeholder for existing sections I–VI. It cannot alone evidence their content or absence.',
         'next': 'Locate the referenced earlier sections and compare existing runtime/other books; do not manufacture replacement history.'},
        {'id': 'COS-A03', 'kind': 'audience-projection-risk', 'evidence': {'byteIdenticalPaths': runtime_paths,
            'import': lines(viewer, 'import lore from'), 'render': lines(viewer, '{activeSongSection.body}'),
            'entryImport': lines('src/app/page.tsx', 'import CosmologyViewer'), 'entryRender': lines('src/app/page.tsx', '<CosmologyViewer'),
            'boundary': lines('DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md', 'Director-Only Truth')},
         'finding': 'The root and review-build runtime JSON are byte-identical to the Director-labeled unfiltered copy. The client component imports the data and renders selected chapter bodies through the entrypoint.',
         'limits': 'Static source evidence only. No live deployment, user authentication, compiled bundle or actual player disclosure is asserted. Developer/owner tooling does not become a certified player export.',
         'next': 'Compare exact chapter passages against knowledge/revelation rules before preparing a separate player projection.'},
        {'id': 'COS-A04', 'kind': 'candidate-theology-versus-fact-presentation-conflict',
         'evidence': [lines(owner, 'Lumina/Umbra as theological abstractions'), lines(folk, 'not literal primordial beings'), lines(viewer, 'Primordial abyssal depth paired with Lumina'), lines(viewer, 'Primordial radiant counterpart to Umbra')],
         'finding': 'The recorded folk-religion treatment explicitly uses theological abstractions, while two component glossary summaries speak in an unqualified primordial register.',
         'next': 'Ask whether the glossary is intended as attributed in-world belief; keep both source passages and do not silently reconcile literal cosmology.'},
        {'id': 'COS-A05', 'kind': 'conflicting-historical-status-notes',
         'evidence': [lines(folk, 'applied 2026-07-31'), lines(folk, 'Appendix B patch is TODO, not performed')],
         'finding': 'The same document records the rulebook patch as applied and later repeats a TODO/not-performed status. These cannot independently prove current publication state.',
         'next': 'Compare the actual rulebook and patch report before correcting navigation/status. This is not a finding that the patch is absent.'},
        {'id': 'COS-A06', 'kind': 'unresolved-authorial-dependency',
         'evidence': [lines('docs/mechanics/SILENT_ONES_CANON.md', '**Peace trigger**'), lines('docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md', '| G2 |')],
         'finding': 'Recorded source notes leave the peace trigger and some endgame identity relations unresolved; the owner lock prohibits inventing those links.',
         'next': 'Check actual notebook/other authoritative evidence for a later owner answer, otherwise isolate exact choices for the owner. No numerical threshold, identity collapse or replacement cosmology is adopted.'},
    ]
    work.mkdir()
    for row in inventory:
        p = G/row['path']; dest = work/'sources'/row['path']; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes()); assert sha(dest.read_bytes()) == row['sha256']
    report = {'reviewId': 'COSMOLOGY-SOURCE-AUTHORITY-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'prepared-not-sent; first source/authority pass only', 'audience': 'owner-and-Director-review-only',
        'deliveredBaselineCommit': BASE, 'remoteMainReverifiedBeforeInventory': BASE,
        'sourceFiles': inventory, 'byteIdenticalGroups': [{'sha256': h, 'paths': names} for h, names in by_hash.items() if len(names)>1],
        'categoryLimit': 'Inventory categories are not new canon authority or approval.',
        'coverageLimit': 'Selected current sources and counterparts only. Full historical inventory, full passage adjudication, class/soul/death/plane dependencies and actual notebook discussion remain required.',
        'sourceInformationDeleted': 0, 'sourceFilesChanged': 0, 'newCosmologyAdopted': False, 'fullCosmologyReviewed': False}
    (work/'SOURCE_INVENTORY.json').write_bytes(encoded(report))
    (work/'DOCX_PASSAGE_INDEX.json').write_bytes(encoded({'scope': 'Exact ordered text runs by XML part/paragraph; full original DOCX supplied. No audience or truth classification inferred.', 'documents': paragraphs}))
    (work/'FINDINGS.json').write_bytes(encoded({'status': 'observations-and-questions; no resolutions adopted', 'findings': findings}))
    request = '''COSMOLOGY-SOURCE-AUTHORITY-01 — first careful post-push source conference

The owner asked us to review cosmology extremely carefully and only after pushing to GitHub. Their later explicit request to push completed work produced the verified progress-backup commit a3f75a0ce577f51bd39153a872ef05ba9e877642. Remote main was reverified before this inventory. This is not final whole-game acceptance. Finish the separately submitted feat-copy source question before taking this packet; do not mix the two rule domains.

All supplied current source files match that delivered commit byte-for-byte. The packet contains full originals and recorded owner-lock/registry/boundary/current-consumer counterparts, exact DOCX text-run positions, and six evidence-linked observations. No source doctrine has been altered. This packet itself is owner/Director material.

First establish which passages have which authority: recorded owner decisions, established Director truth, in-world belief, intentionally unresolved mysteries, original unpromoted documents, historical summaries, and provisional runtime presentation. Neither registry currently has a dedicated general cosmology domain; do not invent new authority or assume a root drop is approved. Preserve the existing domain-specific authority and the original words.

Please give a source-cited disposition for COS-A01–06. Distinguish actual contradictions from audience/register differences and stale status notes. In particular, do not reconcile the folk pantheon literally into the First Choir, turn recorded unknowns into invented facts, merge unresolved endgame identities, or treat ordinary political peace as a decided cosmic threshold. A necessary owner choice should be stated precisely with supported alternatives; check whether this notebook contains a later actual owner answer before asking the owner again.

The original cosmology book is long. Read complete relevant passages, use the indexed paragraphs to cite them, and state what you have and have not covered. An automated search or matching byte hash is not a complete semantic review. The runtime/Director-byte match is a source-presentation concern, not proof of a live leak or a certified player build. Keep intentional revelation progression separate from truth and belief.

Return a downloadable JSON/text authority and issue register, with exact supporting passages and file hashes, dispositions, unresolved dependencies and the next ordered comparison work across creation, gods/pantheons, planes, souls/death/resurrection, history, divine/class powers and campaign revelations. No source replacements, public projection, deletion or completed cosmology claim is requested at this first conference. Any later proposed change must be separate, guarded, source-linked and consequence-checked before incorporation.
'''
    (work/'REQUEST.txt').write_text(request, encoding='utf-8', newline='\n')
    (work/'BASELINE_PUSH_RECEIPT.json').write_bytes((G/'docs/audit/2026-10-14/github-snapshot/PUSH_RECEIPT.json').read_bytes())
    (work/'prepare_cosmology_source_authority_01.py').write_bytes(Path(__file__).read_bytes())
    manifest = {p.relative_to(work).as_posix(): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in sorted(work.rglob('*')) if p.is_file()}
    (work/'PACKAGE_MANIFEST.json').write_bytes(encoded(manifest))
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(work.rglob('*')):
            if p.is_file(): z.write(p, p.relative_to(work).as_posix())
    with zipfile.ZipFile(archive) as z:
        for name, b in manifest.items():
            raw = z.read(name); assert len(raw) == b['bytes'] and sha(raw) == b['sha256'], name
    for row in inventory: assert info(G/row['path'])['sha256'] == row['sha256']
    receipt.write_bytes(encoded({'reviewId': report['reviewId'], 'recordedAtUtc': report['recordedAtUtc'], 'status': report['status'],
        'archive': info(archive), 'manifest': info(work/'PACKAGE_MANIFEST.json'), 'sourceInventory': info(work/'SOURCE_INVENTORY.json'),
        'passageIndex': info(work/'DOCX_PASSAGE_INDEX.json'), 'findings': info(work/'FINDINGS.json'), 'request': info(work/'REQUEST.txt'),
        'sourceFilesVerifiedAgainstDeliveredCommit': len(inventory), 'payloadsVerified': len(manifest),
        'findingsCount': len(findings), 'doctrineChanges': 0, 'fullCosmologyReviewed': False, 'sentToGpt': False, 'sourceInformationDeleted': 0}))
    print(json.dumps({'receipt': info(receipt), 'archive': info(archive), 'sourceFiles': len(inventory), 'payloads': len(manifest), 'findings': len(findings), 'doctrineChanges': 0}))

if __name__ == '__main__': main()
