"""Preserve then correct the existing total-level rule in the legacy evidence helper."""
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
p=R/'tools/feat_exact_01_remaining_owned_chains.py'
folder=A/'before-feat335-curse-capacity-followthrough'
out=A/'FEAT335_CURSE_CAPACITY_DERIVED_OPERATIONS.json'
assert not folder.exists() and not out.exists()

def info(path):
 b=path.read_bytes();return {'path':path.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}

before=p.read_bytes();old=b"additions = {'marks': [], 'markCapacity': 2 if level >= 10 else 1}"
new=b"additions = {'marks': [], 'markCapacity': 2 if sum(self.pay.current_classes.values()) >= 10 else 1}"
assert before.count(old)==1
folder.mkdir();copy=folder/p.name;copy.write_bytes(before)
binding={**info(p),'preservedCopy':copy.relative_to(G).as_posix()}
p.write_bytes(before.replace(old,new,1))
result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'reason':'Curse Channeling current source and FW06 specify total level10, not the level of a banked feat opportunity. KEEP existing rule; initialize capacity from current attained total. No marks, riders, payments or source text changed.',
 'changes':[{'before':binding,'after':info(p),'guardedBefore':old.decode(),'guardedAfter':new.decode()}],
 'newGameRules':0,'sourceInformationDeleted':0}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
(folder/'PRESERVATION_MANIFEST.json').write_text(json.dumps([binding],indent=2)+'\n',encoding='utf-8')
print(json.dumps(info(out)))
