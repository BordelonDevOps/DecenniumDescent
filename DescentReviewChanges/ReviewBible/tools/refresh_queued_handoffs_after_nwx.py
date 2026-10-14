"""Preserve queued source packets and supply completed crafting/teaching evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def sha(p):
    return digest(p.read_bytes())

def rel(p):
    return p.relative_to(G).as_posix()

SPECS = [
    ('HIGHER_RANK_SPELL_FILE_HANDOFF', 322, '435 higher-rank spell identities',
     'Resolve the 388 pre-push mechanical questions against their complete source clauses. The 47 named post-push entries remain literal receipts. Preserve ranks/access, source bindings, counterpart distinctions and focused question IDs. No other game supplies default spell mechanics.'),
    ('FEAT_COMPLETE_FILE_HANDOFF', 236, '327 pending feats',
     'Resolve all nine focused source cohorts and their exact feat identities. Preserve the eight already-reviewed feats. Crafting source decisions supply current task, research and device interfaces; they do not approve any pending feat. Retain original ability-score benefits, prerequisites, category, restrictions and every effect clause; mark added operating detail NEW.'),
    ('BESTIARY_COMPLETE_FILE_HANDOFF', 337, '67 known dossiers and their material/recipe interfaces',
     'Retain the 66 printed stat blocks, 26 public source dossiers, full historical/current pairs and every unresolved material label, unit, yield and recipe reference. Do not infer equivalence by stripping tier suffixes or substituting similar names. Completed recipes give actual output and input procedures, not automatic availability or creature approval. Five sealed dossiers remain containment/routing evidence only.'),
    ('EXPEDITION_COMPLETE_FILE_HANDOFF', 161, '26 expedition-to-Haven cases',
     'Resolve FL-01–26 using the supplied preparation, 126 Player and 260 Core paragraphs, 21 loop sections and 22 governing excerpts. Preserve actual Supply, Pressure, travel, extraction, transport, settlement and reputation distinctions. The reviewed teaching guides explain these systems but do not independently authorize missing mechanics or close whole-game flow.'),
]

def main():
    summary = A / 'QUEUED_HANDOFFS_AFTER_NWX_REFRESH.json'
    assert not summary.exists(), 'Do not overwrite a completed refresh'
    advanced_path = R / 'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json'
    onboarding_path = R / 'docs/playtest/ONBOARDING_REVIEW_STATUS.json'
    advanced, onboarding = read(advanced_path), read(onboarding_path)
    assert advanced['status'].startswith('REVIEWED')
    assert onboarding['status'].startswith('FULFILLED')
    assert len(advanced['artifactHashes']) == 14
    assert len(onboarding['manuscriptHashes']) == 6
    assert all(sha(G/p) == h for p,h in advanced['artifactHashes'].items())
    assert all(sha(G/p) == h for p,h in onboarding['manuscriptHashes'].items())
    assert sha(G/onboarding['receipt']) == onboarding['receiptSha256']
    fulfillment = read(G/onboarding['receipt'])
    assert fulfillment['completionGateSatisfied']
    assert sha(G/fulfillment['verdictFile']) == fulfillment['verdictSha256']
    promotion = read(A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json')
    assert promotion['authority']['completionGateSatisfied']
    assert sha(G/promotion['authority']['verdictFile']) == promotion['authority']['sha256']
    navigation = read(A/'ADVANCED_PROMOTION_NAVIGATION_RECEIPT.json')
    common = {G/p for p in advanced['artifactHashes']} | {G/p for p in onboarding['manuscriptHashes']}
    common.update([advanced_path, onboarding_path, G/onboarding['receipt'],
                   G/fulfillment['verdictFile'], G/promotion['authority']['verdictFile'],
                   A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json',
                   A/'ADVANCED_167_EXACT_COMPLETION_VALIDATION.json',
                   A/'ADVANCED_PROMOTION_NAVIGATION_RECEIPT.json', Path(__file__).resolve()])
    allowed = set(onboarding['manuscriptHashes']) | set(navigation['previousProtectedNavigationFilesUpdated'])
    allowed |= {rel(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json'), rel(R/'docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md')}
    old_joint = read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')
    assert old_joint['sourceVerdictPending'] is False
    assert sha(A/old_joint['verdictFile']) == old_joint['verdictSha256'] if '/' not in old_joint['verdictFile'] else sha(G/old_joint['verdictFile']) == old_joint['verdictSha256']
    plans = []
    for prefix, expected, scope, instructions in SPECS:
        old_path = A/f'{prefix}_PREPARATION.json'
        old = read(old_path)
        archive = A/old['bundleFile'].replace('_v1.zip','_v2.zip')
        out = A/f'{prefix}_V2_PREPARATION.json'
        notes = A/f'{prefix}_V2_SCOPE.md'
        backup = A/'queued-before-nwx-refresh'/prefix.lower()
        assert not any(p.exists() for p in [archive, out, notes, backup])
        assert len(old['currentFileHashes']) == expected
        assert sha(A/old['bundleFile']) == old['bundleSha256']
        changes = []
        with zipfile.ZipFile(A/old['bundleFile']) as z:
            assert z.testzip() is None
            for name, previous in old['currentFileHashes'].items():
                data = z.read(name)
                assert digest(data) == previous
                current = sha(G/name)
                if current != previous:
                    assert name in allowed, ('Unreviewed dependency drift',name)
                    if name in onboarding['manuscriptHashes']:
                        assert current == onboarding['manuscriptHashes'][name]
                        authority = onboarding['receipt']
                    elif name in navigation['previousProtectedNavigationFilesUpdated']:
                        pair = navigation['previousProtectedNavigationFilesUpdated'][name]
                        assert previous == pair['oldSha256'] and current == pair['currentSha256']
                        authority = rel(A/'ADVANCED_PROMOTION_NAVIGATION_RECEIPT.json')
                    else:
                        authority = rel(A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json')
                    changes.append({'file':name,'oldSha256':previous,'currentSha256':current,
                                    'preservedAt':rel(backup/name),'authority':authority,'oldBytes':data})
        plans.append((prefix,old_path,old,archive,out,notes,backup,changes,scope,instructions))
    spells = read(R/'data/public/spell_playtests/catalog.json')['spells']
    higher = {s['id'] for s in spells if s['operational'] is None and min(x['rank'] for x in s['classAccess'].values()) >= 4}
    assert higher == {s['spellId'] for s in plans[0][2]['selectedMembership']}
    assert len(higher) == 435 and sum(s['operational'] is not None for s in spells) == 276
    reports = []
    for prefix,old_path,old,archive,out,notes,backup,changes,scope,instructions in plans:
        for change in changes:
            p = G/change['preservedAt']; p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(change.pop('oldBytes'))
            assert sha(p) == change['oldSha256']
        notes.write_text(f'''# Refreshed source evidence: {scope}

Prepared and UNSENT. This v2 supplies every v1 source path at its current hash, plus complete historical copies of each changed dependency. The v1 archive and preparation remain unchanged. Its original membership and question IDs still control scope; no queued entry gains approval from this refresh.

The advanced-crafting prerequisite is complete: all 167 advanced cards (100 public), hence all 687 recipes (433 public), have passed their authored-operational review. The fourteen final artifacts, exact AEX verdict and fulfillment evidence are supplied in full. The six onboarding/charter manuscripts also completed NWX-01–06 with sixteen amendments, 200 immutable-source checks and eighteen focused adjudications. These teaching/editorial labels add no rule, spell, feat, creature, runtime or human-balance approval.

{instructions}

Read ADVANCED_CRAFT_REVIEW_STATUS.json and ONBOARDING_REVIEW_STATUS.json for current authority. Earlier pending-status labels in frozen preparations and submissions remain historical. The v2 preparation lists each changed file, its preserved old bytes and the completed review that explains the new version. Original source objects and their pending catalog identities remain unchanged. Public and Director audiences retain their respective boundaries.

Language and communication is currently in its source conference. Before dispatching this packet, incorporate any completed language decisions and any intervening spell/feat/profile decisions affecting its actual subjects, then compare all hashes again. This revision is evidence preparation, not a claim that those dependencies are settled. Return finite decisions mapped to the original cases, name actual conflicting sources, and label missing operational details NEW. Preserve literal cosmology receipts without interpretation.

Whole-game flow remains open. The final joint flow review precedes the owner-authorized GitHub push; verified remote commit precedes careful cosmology review. Nothing was deleted or pushed by this refresh.
''',encoding='utf-8')
        files = {G/p for p in old['currentFileHashes']} | common | {notes,old_path}
        files.update(G/c['preservedAt'] for c in changes)
        manifest = {rel(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=rel)}
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            z.writestr('README_V2.md',f'Read {rel(notes)} first. Prepared and UNSENT. Full historical/current evidence is included. No new approvals.\n')
            z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
            for p in sorted(files,key=rel): z.write(p,rel(p))
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert len(z.namelist()) == len(set(z.namelist())) == len(manifest)+2
            assert all(len(z.read(n)) == m['bytes'] and digest(z.read(n)) == m['sha256'] for n,m in manifest.items())
        report = {'status':'PASS complete evidence refresh; UNSENT', 'preparedAtUtc':datetime.now(timezone.utc).isoformat(),
                  'scope':scope,'originalPreparation':rel(old_path),'originalPreparationSha256':sha(old_path),
                  'originalBundle':old['bundleFile'],'originalBundleSha256':old['bundleSha256'],
                  'originalPayloadFiles':old['payloadFiles'],'unchangedOriginalDependencies':old['payloadFiles']-len(changes),
                  'historicalCurrentPairs':changes,'allOriginalBytesPreserved':True,
                  'completedAdvancedArtifacts':14,'completedTeachingManuscripts':6,
                  'sourceMembershipUnchanged':True,'bundleFile':archive.name,'bundleBytes':archive.stat().st_size,
                  'bundleSha256':sha(archive),'payloadFiles':len(manifest),'zipRoundtripVerified':True,
                  'currentFileHashes':{p:m['sha256'] for p,m in manifest.items()},
                  'sent':False,'newApprovals':0,'sourceInformationDeleted':0,'runtimeChanged':False,
                  'cosmologyReviewed':False,'nextAction':'Incorporate completed language and intervening system decisions, check dependencies, then dispatch the mapped source conference.'}
        out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        reports.append({k:v for k,v in report.items() if k!='currentFileHashes'} | {'preparationFile':rel(out),'preparationSha256':sha(out)})
    summary.write_text(json.dumps({'status':'PASS four queued source handoffs refreshed; UNSENT','packets':reports,
                                  'newApprovals':0,'sourceInformationDeleted':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{'scope':x['scope'],'files':x['payloadFiles'],'changedHistoricalPairs':len(x['historicalCurrentPairs']),
                       'archive':x['bundleFile'],'sha256':x['bundleSha256'],'bytes':x['bundleBytes']} for x in reports],indent=2))

if __name__ == '__main__':
    main()
