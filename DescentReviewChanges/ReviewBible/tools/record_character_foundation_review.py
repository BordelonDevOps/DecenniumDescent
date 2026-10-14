"""Record the conditional exact approval after its two wording repairs."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

guide=ROOT/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md'
text=guide.read_text(encoding='utf-8')
assert 'Record one unspent Hit Die of that size.' in text
assert 'Previously spent Hit Dice remain spent; gaining this die does not refresh any earlier die.' in text
assert 'that grant provides no additional proficiency. Character creation, multiclass entry or advancement remains legal.' in text
assert 'record the unresolved selection' not in text
reply=(AUDIT/'GPT_CHARACTER_FOUNDATION_EXACT_REVIEW_BROWSER.txt').read_text(encoding='utf-8')
assert 'After the two wording repairs above, approve all three artifacts' in reply
assert 'REVIEWED CHARACTER FOUNDATION' in reply
before_packet=(AUDIT/'CODEX_CHARACTER_FOUNDATION_EXACT_REVIEW.txt').read_text(encoding='utf-8')
before_json=json.loads(before_packet.split('FULL ARTIFACT data\\playtest\\character_foundation.json SHA256 ',1)[1].split('\n\n',1)[1])
data=json.loads((ROOT/'data/playtest/character_foundation.json').read_text(encoding='utf-8'))
assert before_json['classes']==data['classes']
validation=json.loads((ROOT/'docs/mechanics/CHARACTER_FOUNDATION_VALIDATION.json').read_text(encoding='utf-8'))
assert validation['status']=='PASS' and not validation['changedProtectedFiles']
files=[guide, ROOT/'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md', ROOT/'data/playtest/character_foundation.json', ROOT/'tools/character_foundation.py']
status={'status':'REVIEWED CHARACTER FOUNDATION — authored operational PLAYTEST candidate',
 'sourceConferenceTurn':'93aa40e3-89e9-46cd-bd22-d70cb3e244e1',
 'exactReviewTurn':'d1bc9c3b-6f5a-4aed-a6ad-d39d5cdd933f',
 'approvalCondition':'Exact review expressly approves all three manuscripts after the two requested procedural repairs.',
 'repairsApplied':['Exhausted legal skill/tool choices give no additional proficiency and never block advancement; no substitute or banked grant.','Initial Hit Die and each newly acquired level die are unspent; old spent dice remain spent.'],
 'classRowsMechanicallyUnchangedFromExactSubmission':True,
 'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_CHARACTER_FOUNDATION_CONFERENCE.md','docs/audit/2026-10-08/full-game/GPT_CHARACTER_FOUNDATION_EXACT_REVIEW_BROWSER.txt'],
 'files':[{'path':str(p.relative_to(GAME)).replace('\\','/'),'sha256':sha(p)} for p in files],
 'validation':{'checks':validation['checks'],'classLevelPoolBindings':validation['classLevelPoolBindings'],'protectedFilesUnchanged':validation['protectedFiles']},
 'unclosedScope':data['unclosedScope'],
 'cosmology':data['cosmology'],'githubPushed':False}
write_json(ROOT/'docs/mechanics/CHARACTER_FOUNDATION_REVIEW_STATUS.json',status)
subpath=AUDIT/'CHARACTER_FOUNDATION_EXACT_SUBMISSION.json'
sub=json.loads(subpath.read_text(encoding='utf-8'));sub.update(status='review-complete-two-requested-repairs-applied',responseTurnId=status['exactReviewTurn'],finalStatusPath='DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_REVIEW_STATUS.json');write_json(subpath,sub)

ledger_path=ROOT/'data/playtest/game_development_coverage.json'
ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
scope='Mechanical foundation and advancement connection reviewed: all17 class HD/saves/proficiencies/skill lists/wealth, total vs class levels, multiclass entry/RP/strain, no-healing advancement and new unspent Hit Die. Two exact repairs applied;57 reference checks,340 pool bindings,127 protected files unchanged. Full ancestry/background/equipment and live companion parity remain open.'
for row in ledger['aspects']:
    if row['number'] not in [0,4,5,6,7,9,13,15,60]: continue
    for field,paths in {
        'sourceEvidence':['docs/audit/2026-10-08/full-game/CHARACTER_FOUNDATION_SOURCE_EVIDENCE.json'],
        'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md','DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md','DescentReviewChanges/ReviewBible/data/playtest/character_foundation.json'],
        'reviewEvidence':status['reviewEvidence']+['docs/audit/2026-10-08/full-game/GPT_CHARACTER_FOUNDATION_EXACT_REVIEW.md'],
        'validationEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_VALIDATION.json','DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_REVIEW_STATUS.json']}.items():
        for path in paths:
            if path not in row[field]:row[field].append(path)
    if scope not in row.setdefault('completedScopes',[]):row['completedScopes'].append(scope)
    if row['number'] in [4,6,7]:row['status']='foundation-reviewed-broader-domain-open'
    if row['number']==4:row['openIssues']=['Finish complete ancestry/variant traits, background packages/features, actual equipment and all remaining prerequisite-dependent options before certifying blank-sheet legality for every combination.']
    if row['number']==5:row['openIssues']=['Implement/reconcile full source-aware character state, chronological HP/Hit Dice, acquisition order, class choices, equipment and spell preparation in the live companion; the new dataset is not that runtime.']
    if row['number']==6:row['openIssues']=['Finish full mixed-class acquisition/retraining/replacement-PC procedures and all option dependencies; foundation math and class-level boundaries alone do not close every1–20 build.']
    if row['number']==7:row['openIssues']=['Finish all mixed-class source interactions and live state/acquisition parity; entry, proficiency, mergedRP and shared strain rules are now explicit.']
write_json(ledger_path,ledger)

start=GAME/'START_HERE.md';old=start.read_text(encoding='utf-8')
if 'Character foundation |' not in old:
    old=old.replace('| Ordinary spells |','| [Character foundation](DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md) | All17 class foundations, advancement and multiclass rules jointly reviewed;57 reference checks pass | Full ancestry/background/equipment and companion integration |\n| Ordinary spells |',1)
paragraph='The latest whole-game manuscript is the [reviewed character foundation](DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md), with [all17 class tables](DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md). It resolves starting proficiencies/skills/wealth, HP advancement, class versus total levels, multiclass entry and shared RP/strain. Both GPT-requested wording repairs are applied;57 reference checks,340 class-level pool bindings and127 unchanged protected files support this bounded review. Full ancestry/background/equipment and live companion work remain open.\n\n'
if paragraph not in old:
    old=old.replace('The latest completed manuscript work is',paragraph+'The preceding spell manuscript work is',1)
start.write_text(old,encoding='utf-8')

legacy=ROOT/'docs/mechanics/CHARGEN_PROGRESSION.md';old=legacy.read_text(encoding='utf-8')
needle='**Current campaign-playtest use:** this July guide documents'
new='**Current campaign-playtest use:** begin with the [reviewed creation and advancement foundation](CHARACTER_CREATION_PLAYTEST.md) and [17-class tables](CHARACTER_FOUNDATION_TABLES.md). This July guide documents'
if needle in old:old=old.replace(needle,new,1)
legacy.write_text(old,encoding='utf-8')
quick=ROOT/'docs/mechanics/QUICKSTART_LEVEL_1.md';old=quick.read_text(encoding='utf-8')
notice='Use the [reviewed character foundation](CHARACTER_CREATION_PLAYTEST.md) and [17-class tables](CHARACTER_FOUNDATION_TABLES.md) for starting statistics, advancement and multiclass rules. Full ancestry/background/equipment reconciliation remains in progress.\n\n'
if notice not in old:
    title,rest=old.split('\n',1);old=title+'\n\n'+notice+rest.lstrip('\n')
quick.write_text(old,encoding='utf-8')

audit=AUDIT/'REVIEW_STATUS.md';old=audit.read_text(encoding='utf-8')
entry='''\n\n## Character foundation and advancement connection reviewed

The [source conference](GPT_CHARACTER_FOUNDATION_CONFERENCE.md) and [exact manuscript review](GPT_CHARACTER_FOUNDATION_EXACT_REVIEW.md) settle all17 starting class profiles,20 basic skills,ability generation,HP/Hit Dice,wealth,advancement and multiclass RP/strain. All17 class rows passed without repairs. Both requested procedure repairs are applied: exhausted skill/tool choices grant no extra proficiency without blocking advancement; newly acquired Hit Dice are unspent while prior spent dice stay spent.

[Creation and advancement](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md) and [class tables](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md) are linked from Start Here and the existing guides. [57 reference checks](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_VALIDATION.json) pass, including340 exact source-pool bindings;127 protected book/class/companion/spell files are unchanged. The [review status](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_REVIEW_STATUS.json) records exact artifact hashes and bounded scope. This does not close full character creation, all mixed builds, live companion parity or human balance.

The next mechanical source pass has located14 ancestry trait sections and20 background packages in the [source index](ANCESTRY_BACKGROUND_MECHANICAL_SOURCE_INDEX.json). Equipment remains a real next dependency. The ordinary spell/feat counts are unchanged at269/848 and8/335. No source was deleted and GitHub was not pushed. Cosmology remains deferred until after verified authorized GitHub delivery.
'''
if '## Character foundation and advancement connection reviewed' not in old:audit.write_text(old+entry,encoding='utf-8')
print('Recorded joint foundation approval, applied repairs, linked entrypoints and retained open whole-game scope.')
