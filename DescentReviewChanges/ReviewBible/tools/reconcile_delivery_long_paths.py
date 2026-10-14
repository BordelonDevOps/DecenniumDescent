"""Reconcile stat failures without rewriting the original delivery screening."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
source = A / 'GITHUB_DELIVERY_SIZE_SCREENING_2026-10-11.json'
out = A / 'GITHUB_DELIVERY_LONG_PATH_RECONCILIATION_2026-10-11.json'
assert not out.exists(), 'Preserve existing reconciliation'
d = json.loads(source.read_text(encoding='utf-8'))
recovered = []
errors = []
for name in d['vanishedDuringScan']:
    try:
        s = os.stat('\\\\?\\' + name)
        relative = Path(name).relative_to(G).as_posix()
        recovered.append({'path': relative, 'pathCharacters': len(name),
                          'bytes': s.st_size, 'lastModifiedNs': s.st_mtime_ns})
        key = relative.split('/')[0]
        group = d['topLevelGroups'].setdefault(key, {'files': 0, 'bytes': 0, 'above100MiB': 0})
        group['files'] += 1
        group['bytes'] += s.st_size
        group['above100MiB'] += s.st_size > 100 * 1024 * 1024
    except OSError as e:
        errors.append({'path': name, 'error': str(e)})
report = {
    'status': 'All initial stat failures resolved as Windows long paths' if not errors else 'Some paths still unresolved',
    'atUtc': datetime.now(timezone.utc).isoformat(),
    'originalScreening': str(source),
    'originalSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'correction': 'The original vanishedDuringScan label was inaccurate: ordinary stat could not access long Windows paths. Extended-length path stat verifies their presence. Original report is preserved unchanged.',
    'scope': 'Addendum to the same rg enumeration and its explicit directory exclusions; not a new enumeration, complete backup, deletion finding or publication manifest.',
    'recoveredCount': len(recovered), 'recoveredBytes': sum(x['bytes'] for x in recovered),
    'correctedFileCount': d['fileCount'] + len(recovered),
    'correctedTotalBytes': d['totalBytes'] + sum(x['bytes'] for x in recovered),
    'correctedTopLevelGroups': d['topLevelGroups'],
    'additionalAbove100MiB': [x for x in recovered if x['bytes'] > 100 * 1024 * 1024],
    'additionalAbove50Through100MiB': [x for x in recovered if 50 * 1024 * 1024 < x['bytes'] <= 100 * 1024 * 1024],
    'recoveredFiles': recovered, 'unresolved': errors,
    'sourceInformationDeleted': 0, 'filesMoved': 0, 'pushPerformed': False,
    'deliveryCheckout': d['deliveryCheckout'],
}
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: report[k] for k in ['status', 'recoveredCount', 'recoveredBytes', 'correctedFileCount', 'correctedTotalBytes', 'additionalAbove100MiB', 'unresolved']}, indent=2))
