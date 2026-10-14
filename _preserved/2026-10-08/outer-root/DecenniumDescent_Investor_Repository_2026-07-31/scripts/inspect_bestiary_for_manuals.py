"""Inspect Bestiary.xlsx Monsters sheet + bestiary JSON for manual generation."""
from pathlib import Path
import json
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
wb = openpyxl.load_workbook(ROOT / "Bestiary.xlsx", read_only=True, data_only=True)
ws = wb["Monsters"]
rows = ws.iter_rows(values_only=True)
header = next(rows)
print("COLS", len(header))
print(header)
count = 0
sample = []
for r in rows:
    if r and r[0]:
        count += 1
        if len(sample) < 3:
            sample.append(r[:15])
print("monster rows", count)
for s in sample:
    print(s)
wb.close()

jp = ROOT / "src" / "bestiary_data_full.json"
data = json.loads(jp.read_text(encoding="utf-8"))
if isinstance(data, list):
    print("json monsters", len(data))
    print("keys", list(data[0].keys())[:40])
    c = data[0].get("combat")
    print("combat sample", c)
elif isinstance(data, dict):
    print("top", list(data.keys())[:20])
    m = data.get("monsters") or data.get("entries") or []
    print("len", len(m))
    if m:
        print("keys", list(m[0].keys())[:40])
