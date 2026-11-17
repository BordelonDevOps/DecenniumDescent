"""Create disposable hostile saves with recomputed checksums and declaration hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(exist_ok=False)
data = args.source.read_bytes()
digest = lambda b: hashlib.sha256(b).hexdigest()
assert hashlib.sha256(data[:-32]).digest() == data[-32:]
assert struct.unpack_from('<i', data, 4)[0] == 113
n = struct.unpack_from('<i', data, 8)[0]
fingerprint = data[12:12+n].decode()
parent_prefix = b'TEST_ONLY.bishop-entry-v1-'
parent_offset = data.rindex(parent_prefix)
parent = data[parent_offset:parent_offset+len(parent_prefix)+64].decode()
binding = parent_offset - 5
assert data[binding] == 18
old_digest_offset = parent_offset + len(parent) + 4
old_digest = data[old_digest_offset:old_digest_offset+64].decode()
cells = [(2,1,1,0,0,0),(6,1,0,0,1,0),(7,0,1,0,0,0),(9,0,0,1,0,0),(11,0,1,1,1,1)]
terrain = [(5,2,2),(6,2,3)]
encode_map = lambda w, c: struct.pack('<iii',w,5,len(c)) + b''.join(struct.pack('<ii4B',*x) for x in c)
map_bytes = encode_map(12,cells)
assert data.count(map_bytes) == 1
map_offset = data.index(map_bytes)
semantics = 'chebyshev-5ft|exact-path-sight-intervals-v2|channels-independent|all-channel-anchor-support|movement-two-unsupported-sides|ordinary-cardinal|tactical-diagonal|destination-terrain|known-static-map-only'
def declaration(w,c,t):
    value = '|'.join(('TEST_ONLY.shared-declared-geometry.v1','187b46f8-dfeb-5c95-9554-6c7e0b6b9113',semantics,f'{w}x5',';'.join(','.join(map(str,x)) for x in c),';'.join(','.join(map(str,x)) for x in t)))
    return digest(value.encode())
assert declaration(12,cells,terrain) == old_digest
assert fingerprint == 'TEST_ONLY.declared-geometry-v1-' + digest((parent+'|'+old_digest).encode())
rows = []
def save(name,payload,description):
    hostile = bytes(payload) + hashlib.sha256(payload).digest()
    path = args.output/(name+'.ddsave')
    path.write_bytes(hostile)
    rows.append(dict(name=path.name,sha256=digest(hostile),bytes=len(hostile),description=description,recomputedChecksum=True))
for name,width,c,t in [('width',13,cells,terrain),('terrain',12,cells,[(5,2,1),(6,2,3)]),('channels',12,[cells[0],(6,1,1,0,1,0),*cells[2:]],terrain)]:
    forged = bytearray(data[:-32])
    forged[map_offset:map_offset+len(map_bytes)] = encode_map(width,c)
    assert struct.unpack_from('<i',forged,len(forged)-28)[0] == 2
    forged[-24:] = b''.join(struct.pack('<iii',*x) for x in t)
    revised = declaration(width,c,t)
    forged[old_digest_offset:old_digest_offset+64] = revised.encode()
    forged[12:12+n] = ('TEST_ONLY.declared-geometry-v1-'+digest((parent+'|'+revised).encode())).encode()
    save(name,forged,'Changed approved geometry with a matching attacker-recomputed declaration digest, fingerprint and checksum')
save('missing-binding',data[:binding],'Complete inherited payload but missing mandatory113 appended geometry')
marker=bytearray(data[:-32]);marker[binding]=17
save('wrong-marker',marker,'Wrong geometry marker with an otherwise preserved payload')
(args.output/'manifest.json').write_text(json.dumps(dict(source=str(args.source),sourceSha256=digest(data),scope='Hostile bytes only; execution/rejection verified separately',cases=rows),indent=2)+'\n')
print(json.dumps(dict(generated=len(rows),sourceSha256=digest(data))))
