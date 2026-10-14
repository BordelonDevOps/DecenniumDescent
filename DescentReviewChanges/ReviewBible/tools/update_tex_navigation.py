"""Update current owner navigation after fulfilled TEX, retaining every old page."""
from pathlib import Path
from hashlib import sha256
import json,shutil
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
B=A/'navigation-before-tex-completion';assert not B.exists()
paths=['START_HERE.md','REVIEW_MAP.html','docs/audit/2026-10-08/full-game/GPT_REVIEW_CONTINUATION_HANDOFF.md','docs/audit/2026-10-08/full-game/REVIEW_MAP_BUILD.json','docs/audit/2026-10-08/full-game/REVIEW_MAP_BROWSER_QA.json','DescentReviewChanges/ReviewBible/tools/build_review_map.py']
for rel in paths:
 p=B/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(G/rel,p)
p=G/'START_HERE.md';t=p.read_text('utf-8-sig');old='The next bounded review covers nine teaching artifacts and the Efficient Recycling conflict.'
assert t.count(old)==1
t=t.replace(old,'[All nine teaching artifacts are now reviewed](docs/audit/2026-10-08/full-game/TEACHING_TEX_EXACT_FULFILLMENT.json); TEX-01–04 and the five character-navigation notes are fulfilled. Efficient Recycling does not require enemy cause; its other actual source limits remain. The next source conference covers expedition, transport, social and reputation procedures.')
for before,after,count in [('teaching draft, presentation review pending','reviewed authored teaching/presentation',3),('presentation review remains pending','reviewed authored presentation; human use remains untested',1),('joint presentation review pending','reviewed authored presentation; human use remains untested',1),('[Language worksheet draft]','[Language worksheet]',1),('[48-term glossary draft]','[48-term glossary]',1)]:
 assert t.count(before)==count,(before,t.count(before));t=t.replace(before,after)
anchor='| A Base-class character |';assert t.count(anchor)==1
t=t.replace(anchor,'| Record a character | [Five-page fillable sheet](DescentReviewChanges/ReviewBible/output/pdf/Decennium_Descent_Character_Sheet_Playtest.pdf), [usage instructions](DescentReviewChanges/ReviewBible/docs/playtest/CHARACTER_SHEET_PLAYTEST.md) and [17-class resource reference](DescentReviewChanges/ReviewBible/docs/playtest/CLASS_RESOURCE_REFERENCE.md); reviewed authored presentation |\n'+anchor)
t=t.replace('## Folder map and preserved history','Use the [searchable review map](REVIEW_MAP.html) to find a game area, its current scope, outstanding questions and supporting files. It is an owner/Director navigation aid.\n\n## Folder map and preserved history',1)
p.write_text(t,encoding='utf-8',newline='\n')
p=A/'GPT_REVIEW_CONTINUATION_HANDOFF.md';old=p.read_text('utf-8-sig')
new='''**CURRENT — TEX teaching review fulfilled:** GPT final `cb2e5a59-d467-4439-903f-1af7c37c7838`, TEX-EXACT-2026-10-11, is preserved in the [complete 46-file verdict package](DD_Teaching_9_Exact_Verdict_and_Evidence.zip). [Local fulfillment](TEACHING_TEX_EXACT_FULFILLMENT.json) applies all nine operative replacements in seven files, the controlling Recycling erratum and five navigation notes with the governing chapter’s original LF convention. All29 TE questions and16 authored acceptance expectations are accounted for. Local checks pass:2262 frozen-source,621 strict-amendment,67 focused-reference;162 corrected links resolve. Eight manuscript labels have exact reversible proofs; the five-page/364-field PDF is unchanged. [Current teaching status](../../../../DescentReviewChanges/ReviewBible/docs/playtest/TEACHING_REVIEW_STATUS.json) binds all nine current artifacts. No generic teaching resubmission is needed.

**Resolved interface:** [TC-RECYCLING-01](TC_RECYCLING_01_CONTROLLING_ERRATUM.md) retains the class/lifecycle predicate: enemy cause is not required. Payment, acquisition, original owned non-copy device, no sacrifice, actual postcombat minute, rest allowance, single-consumer debris and source restriction flags remain. Exactly five coverage occurrences moved to preserved resolvedInterfaceIssues; every game-area status stays unchanged. Original TD-13, source cards, recipe arrays/body models, old AEX/LRX hashes and historical receipts are retained. Current AEX status appends the new descendant hashes rather than rewriting old evidence.

**Next source conference:** Refresh and submit the complete expedition-to-Haven package, incorporating the [12 social/faction questions](SOCIAL_FACTION_SOURCE_AUDIT.md), [full unadopted proposal](SOCIAL_FACTION_OPERATING_PROPOSAL.md), [six reputation-preservation subquestions](REPUTATION_PRESERVATION_SOURCE_ADDENDUM.md) and [14 transport questions](TRANSPORT_SOURCE_AUDIT.md). The [transport preparation](TRANSPORT_SOURCE_PREPARATION.json) retains all29 omitted mount/vehicle/service records,54 selected paragraphs/two tables and33 full sources; no transport procedure is yet adopted. FL-23 is one conflict with three source scales, not three independent new systems. Preserve deferred cosmology semantics. Social proposals, including ±3 standing and a 24-hour checkpoint, remain explicitly unadopted.

Ordinary spells remain412 authored reviewed/436 pending; recipes687 internal/433 public reviewed; all original75-area gates retain their prior statuses. Remaining spell/feat/bestiary/Director work, whole-game flow, runtime and human evidence remain open. Actual final joint flow → authorized GitHub push → verified remote → careful cosmology review. No push, deletion or cosmology review has occurred.

**Historical checkpoints below are preserved verbatim. Earlier pending/active labels describe their dates and are superseded by the current fulfilled checkpoint above.**

'''
p.write_text(new+old,encoding='utf-8',newline='\n')
receipt={'scope':'Owner start and current notebook handoff metadata after TEX fulfillment; no rules changes','preservedDirectory':B.relative_to(G).as_posix(),'changed':{rel:{'beforeSha256':sha256((B/rel).read_bytes()).hexdigest(),'afterSha256':sha256((G/rel).read_bytes()).hexdigest()} for rel in paths[:1]+[paths[2]]},'transportProposalStillUnsent':True}
(A/'TEACHING_TEX_NAVIGATION_UPDATE.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt))
