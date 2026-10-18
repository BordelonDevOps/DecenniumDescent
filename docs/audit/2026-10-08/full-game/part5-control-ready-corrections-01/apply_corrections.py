#!/usr/bin/env python3
"""Verify or stage the five bound authored JSON corrections; never edit in place.

Default: validate the bundled baseline and complete before/after operations.
--source-root: validate the corresponding paths in a local repository snapshot.
--output: stage only the five corrected files into a NEW directory.
--reverse: validate corrected inputs and stage the exact original baseline bytes.
This is an artifact staging tool, not a game engine or repository commit tool.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile
from typing import Any

BUNDLE = Path(__file__).resolve().parent

class CorrectionError(ValueError):
    """A binding, pointer precondition, or staging safety check failed."""

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def safe_relative(name: str) -> Path:
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
        raise CorrectionError(f'Unsafe relative path: {name!r}')
    return Path(*p.parts)

def tokens(pointer: str) -> list[str]:
    if not pointer.startswith('/'):
        raise CorrectionError(f'Non-absolute JSON pointer: {pointer!r}')
    return [p.replace('~1', '/').replace('~0', '~') for p in pointer[1:].split('/')]

def at(document: Any, pointer: str) -> Any:
    value = document
    for key in tokens(pointer):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value

def parent_at(document: Any, pointer: str) -> tuple[Any, str]:
    parts = tokens(pointer)
    value = document
    for key in parts[:-1]:
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value, parts[-1]

def edit(document: Any, op: dict[str, Any], reverse: bool = False) -> None:
    parent, key = parent_at(document, op['jsonPointer'])
    kind = op['op']
    if kind == 'replace':
        expected, result = (op['after'], op['before']) if reverse else (op['before'], op['after'])
        actual = parent[int(key)] if isinstance(parent, list) else parent[key]
        if actual != expected:
            raise CorrectionError(f"Full value mismatch at {op['jsonPointer']}")
        if isinstance(parent, list):
            parent[int(key)] = copy.deepcopy(result)
        else:
            parent[key] = copy.deepcopy(result)
    elif kind == 'add' and not isinstance(parent, list):
        if reverse:
            if key not in parent or parent[key] != op['after']:
                raise CorrectionError(f"Reverse-add mismatch at {op['jsonPointer']}")
            del parent[key]
        else:
            if key in parent or op.get('beforeExists') is not False:
                raise CorrectionError(f"Add requires absence at {op['jsonPointer']}")
            parent[key] = copy.deepcopy(op['after'])
    else:
        raise CorrectionError(f'Unsupported operation: {kind!r}')

def prepare(source_root: Path | None = None, reverse: bool = False) -> dict[str, bytes]:
    """Validate every input and operation before returning any output bytes."""
    spec = json.loads((BUNDLE / 'ARTIFACT_BINDINGS.json').read_text(encoding='utf-8'))
    plan = json.loads((BUNDLE / 'POINTER_OPERATIONS.json').read_text(encoding='utf-8'))
    rows = {row['key']: row for row in spec['files']}
    if len(rows) != 5 or plan['fileCount'] != 5 or len(plan['operations']) != plan['operationCount']:
        raise CorrectionError('Unexpected file or operation inventory')
    documents: dict[str, Any] = {}
    raw_inputs: dict[str, bytes] = {}
    for key, row in rows.items():
        rel = safe_relative(row['repositoryPath'])
        source = (source_root / rel) if source_root else BUNDLE / (row['correctedFile'] if reverse else row['baselineFile'])
        if source_root and not source.resolve().is_relative_to(source_root.resolve()):
            raise CorrectionError(f'Source symlink escapes the selected root: {source}')
        raw = source.read_bytes()
        expected_hash = row['correctedSha256'] if reverse else row['sha256']
        expected_len = row['correctedBytes'] if reverse else row['bytes']
        if len(raw) != expected_len or digest(raw) != expected_hash:
            raise CorrectionError(f'BASELINE DRIFT: {row["repositoryPath"]}; no files were staged')
        documents[key] = json.loads(raw)
        raw_inputs[key] = raw
    ordered = reversed(plan['operations']) if reverse else plan['operations']
    for op in ordered:
        key = op['fileKey']
        if key not in rows or op['repositoryPath'] != rows[key]['repositoryPath']:
            raise CorrectionError('Operation file identity mismatch')
        edit(documents[key], op, reverse)
    outputs = {}
    for key, row in rows.items():
        result = encoded(documents[key])
        expected_hash = row['sha256'] if reverse else row['correctedSha256']
        expected_len = row['bytes'] if reverse else row['correctedBytes']
        if len(result) != expected_len or digest(result) != expected_hash:
            raise CorrectionError(f'Complete result binding mismatch: {row["repositoryPath"]}')
        # The reverse also proves exact byte restoration, not only JSON equality.
        outputs[row['repositoryPath']] = result
    return outputs

def stage(outputs: dict[str, bytes], output: Path, source_root: Path | None) -> None:
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise CorrectionError('--output must name a directory that does not exist')
    resolved = output.resolve()
    forbidden = [BUNDLE.resolve()]
    if source_root:
        forbidden.append(source_root.resolve())
    if any(resolved.is_relative_to(root) or root.is_relative_to(resolved) for root in forbidden):
        raise CorrectionError('Output must be separate from both the bundle and source repository')
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.dd-stage-', dir=output.parent))
    try:
        for name, raw in outputs.items():
            dest = staging / safe_relative(name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
        if output.exists():
            raise CorrectionError('Output appeared during staging; refusing overwrite')
        os.rename(staging, output)
    finally:
        if staging.exists():
            shutil.rmtree(staging)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, help='Local snapshot root; default is bundled originals')
    parser.add_argument('--output', type=Path, help='NEW staging directory; omitted means read-only verification')
    parser.add_argument('--reverse', action='store_true', help='Validate corrected inputs and restore original bytes')
    args = parser.parse_args()
    try:
        outputs = prepare(args.source_root, args.reverse)
        if args.output:
            stage(outputs, args.output, args.source_root)
        print(json.dumps({'mode': 'reverse' if args.reverse else 'forward', 'files': len(outputs),
                          'operations': 22, 'result': 'PASS',
                          'stagedTo': str(args.output) if args.output else None,
                          'repositoryModified': False, 'runtimeImplemented': False}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
