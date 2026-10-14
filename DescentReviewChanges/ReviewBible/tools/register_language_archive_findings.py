"""Register the independently confirmed packaging issue without changing submitted bytes."""
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import hashlib
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
paths=[G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json']
backup=A/'navigation-before-language-archive-finding';backup.mkdir()
for p in paths:shutil.copy2(p,backup/p.name)
(backup/'MANIFEST.json').write_text(json.dumps({p.name:{'original':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths},indent=2)+'\n',encoding='utf-8')
start=paths[0].read_text(encoding='utf-8')
needle='Exact candidate approval remains pending. |'
assert needle in start
start=start.replace(needle,'Exact candidate approval remains pending. The [portable archive audit](docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_V1_ARCHIVE_LINK_AUDIT.json) identifies four linked reference files omitted from the ZIP; all four exist locally and are identified for the verdict-fulfillment package. |')
paths[0].write_text(start,encoding='utf-8')
handoff=paths[1].read_text(encoding='utf-8')
note='''**Live exact-review finding (not a final verdict):** GPT confirmed all184 payloads and the460 source checks, then reported four missing linked destinations in the review ZIP. The independent [archive-link audit](LANGUAGE_EXACT_V1_ARCHIVE_LINK_AUDIT.json) reproduces exactly those four missing files: CLASS_PLAYTEST_INDEX.md, PALADIN_OATHS_AND_OATHBREAKERS.md, SCRIBING_CANDIDATE_RECIPE_CARDS.md and TINKERING_CANDIDATE_RECIPE_CARDS.md, all under the review mechanics folder. They exist locally with recorded hashes. The local496 report checked working-tree links; it did not establish archive completeness. Preserve that original report and frozen ZIP. Include all four complete unchanged files when fulfilling the final exact verdict; do not interrupt the active review or resend now. No rule/candidate promotion has occurred.

'''
pos=handoff.index('\n\n')+2;handoff=handoff[:pos]+note+handoff[pos:];paths[1].write_text(handoff,encoding='utf-8')
obs=json.loads(paths[2].read_text(encoding='utf-8'))
obs.update({'atUtc':datetime.now(timezone.utc).isoformat(),'status':'Exact review actively inspecting recipe/source structures; final verdict pending',
 'verifiedLiveFindings':['184 payloads and archive hash verified by GPT','460 source checks reproduced by GPT','four guide-link destinations absent from ZIP but present in working tree'],
 'independentPortableAudit':str(A/'LANGUAGE_EXACT_V1_ARCHIVE_LINK_AUDIT.json'),
 'next':'Await full exact verdict; include four complete missing link targets with bounded corrections. Do not interrupt/resend the active review or alter frozen bytes.'})
paths[2].write_text(json.dumps(obs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded four portable packaging findings; submitted candidate, all sources and acceptance gates unchanged.')
