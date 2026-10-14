"""Check prestige feat refs against feats.js with fuzzy match."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    buf = path.read_bytes()
    if buf[:2] == b"\xff\xfe":
        return buf.decode("utf-16le").lstrip("\ufeff")
    return buf.decode("utf-8", errors="replace")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


feats_text = (ROOT / "src/data/feats.js").read_text(encoding="utf-8")
fnames = {norm(n): n for n in re.findall(r'"name": "([^"]+)"', feats_text)}

rb = read_text(ROOT / "rulebook_output.txt")
refs: set[str] = set()
for line in rb.splitlines():
    if "Feats:" in line:
        chunk = line.split("Feats:", 1)[1]
        for part in re.split(r",\s*", chunk):
            name = part.strip().strip("-").strip()
            if name and len(name) < 60:
                refs.add(norm(name))

print(f"feats={len(fnames)} prestige_refs={len(refs)}")
missing = []
for r in sorted(refs):
    if r in fnames:
        continue
    # substring match
    fuzzy = [fnames[k] for k in fnames if r in k or k in r]
    if fuzzy:
        print(f"FUZZY {r!r} -> {fuzzy}")
    else:
        missing.append(r)

print(f"truly_missing={len(missing)}")
for m in missing:
    print(f"  {m}")
