"""LRX-01: authentic 342-file protection map; no writes or network access.
Copy beside the three working candidate tools, import load_protected_manifest,
and replace their missing-preparation read with load_protected_manifest(G).
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

MANIFEST_SHA256 = '67ece631a37b7fab72db15cc4f6d67215790617ce35ae8def39e25754a00eeba'
SOURCE_ZIP_SHA256 = '5acb3e4c6d9b3652b5731ffc111539a558874285c87dd0952a3398431b896640'
SOURCE_ZIP_BYTES = 29192630

def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result

def _decode(raw):
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError('Original v3 manifest does not match the frozen reviewed manifest')
    result = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_object)
    if not isinstance(result, dict) or len(result) != 342:
        raise ValueError('Exactly 342 original payload records are required')
    return result

def load_protected_manifest(root: Path) -> dict[str, str]:
    root = Path(root).resolve()
    sidecar = root / 'ORIGINAL_SOURCE_V3_FILE_MANIFEST.json'
    original = root / 'docs/audit/2026-10-08/full-game/DD_Low_Rank_Spells_137_Source_Prepared_v3.zip'
    manifests = []
    if sidecar.is_file():
        manifests.append(_decode(sidecar.read_bytes()))
    if original.is_file():
        raw = original.read_bytes()
        if len(raw) != SOURCE_ZIP_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_ZIP_SHA256:
            raise ValueError('Original v3 archive size or SHA256 mismatch')
        with zipfile.ZipFile(original) as z:
            if z.namelist().count('FILE_MANIFEST.json') != 1:
                raise ValueError('Original archive must contain one unambiguous manifest')
            manifests.append(_decode(z.read('FILE_MANIFEST.json')))
    if not manifests:
        raise FileNotFoundError('Need the reviewed root manifest or unchanged original v3 ZIP')
    if any(m != manifests[0] for m in manifests[1:]):
        raise ValueError('Original manifest copies disagree')
    manifest = manifests[0]
    result = {}
    for name, record in manifest.items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name:
            raise ValueError(f'Unsafe original path: {name}')
        file = (root / name).resolve()
        if not file.is_relative_to(root) or not file.is_file():
            raise FileNotFoundError(f'Protected source missing or outside root: {name}')
        if not isinstance(record,dict) or set(record) != {'bytes','sha256'}:
            raise ValueError(f'Invalid manifest record: {name}')
        raw = file.read_bytes()
        if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
            raise ValueError(f'Protected source drift: {name}')
        result[name] = record['sha256']
    return result
