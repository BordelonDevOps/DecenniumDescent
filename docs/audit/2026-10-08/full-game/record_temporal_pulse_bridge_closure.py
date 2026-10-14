"""Bind actual incremental approval to exact code; keep full integration open."""
from pathlib import Path
import hashlib
import json

AUDIT=Path(__file__).resolve().parent
GAME=AUDIT.parents[3]
ROOT=GAME/'DescentReviewChanges/ReviewBible'

def main():
    review=AUDIT/'GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md'
    assert 'no reproducible blocker' in review.read_text(encoding='utf-8')
    manifest=json.loads((AUDIT/'TEMPORAL_PULSE_BRIDGE_REVIEW_MANIFEST.json').read_text(encoding='utf-8'))
    for name in ('tools/temporal_control_playtest_rules.py','tools/validate_temporal_control_playtests.py'):
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==manifest['hashes'][name]
    status=ROOT/'docs/mechanics/TEMPORAL_PULSE_BRIDGE_REVIEW_STATUS.json'
    assert not status.exists()
    status.write_text(json.dumps({
        'status':'REVIEWED / reference-VALIDATED canonical payment and resolved independent-output guards only',
        'independentEvidence':str(review.relative_to(GAME)).replace('\\','/'),
        'reviewedHelperSha256':manifest['hashes']['tools/temporal_control_playtest_rules.py'],
        'testMethods':22,'fullControlPulseRestoration':False,'fullTimeLoopOperational':False,
        'remainingMajorIntegrations':7,'wholeGameClosure':False,'githubPushed':False,
    },indent=2)+'\n',encoding='utf-8')
    p=ROOT/'docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md'
    text=p.read_text(encoding='utf-8').replace(
        'This wording clarification is being returned to the notebook before implementation of the scheduler.',
        'The notebook explicitly [confirmed this distinction and immutable snapshot membership](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md). No currently supplied pulse profile needs a fabricated at-initiative creation exception; native passive abilities instead await their future genuine regular-start events.')
    text=text.replace('Independent code review is pending.',
        'The [actual independent review](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md) approves only these payment/resolved-output bridges. The [review manifest](TEMPORAL_PULSE_BRIDGE_REVIEW_STATUS.json) binds that approval to the exact unchanged helper. The validation JSON retains its original submitted pre-review scope label as evidence; the separate review manifest records the later disposition.')
    p.write_text(text,encoding='utf-8')
    p=ROOT/'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md'
    text=p.read_text(encoding='utf-8')
    text += '\nThe subsequent [control/pulse conference and first implementation bridges](TEMPORAL_CONTROL_PLAYTEST.md) have their own recorded scope: nine source-policy families discussed and22 payment/output checks jointly reviewed. Full nine-family restoration remains unfinished, so the seven missing-integration count is unchanged.\n'
    p.write_text(text,encoding='utf-8')
    p=ROOT/'data/playtest/game_development_coverage.json'
    (AUDIT/'COVERAGE_BEFORE_TEMPORAL_PULSE_BRIDGE_CLOSURE.json').write_bytes(p.read_bytes())
    data=json.loads(p.read_text(encoding='utf-8'))
    for row in data['aspects']:
        if row['id'] not in ('DD-03','DD-08','DD-09','DD-16','DD-18','DD-21','DD-35','DD-63','DD-64'):continue
        row['openIssues']=[x.replace('pass22 focused tests and await independent code review',
            'passed22 focused tests and completed bounded independent code review') for x in row['openIssues']]
        row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[str(review.relative_to(GAME)).replace('\\','/')]))
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=GAME/'START_HERE.md'
    text=p.read_text(encoding='utf-8').replace(
        'its first22 payment/output checks pass and independent code review is in progress.',
        'its first22 payment/output checks pass and have completed joint review. Full control/pulse restoration is still in progress.')
    p.write_text(text,encoding='utf-8')
    note='''
## Bounded pulse payment/output bridge jointly reviewed

[GPT's actual completed review](GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md) finds no reproducible blocker within the22-test payment/resolved-output scope. Exact reviewed helper SHA256: `835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12`. The code and tests remain unchanged from the submitted packet.

The reply also confirms: early failed ordinary maintenance remains pending until its real deadline; exact-due failed upkeep ends immediately; an after-snapshot source cannot acquire snapshot membership; the supplied pulse profiles normally present at initiative have preserved outside-origin schedules. Native abilities exist at capture, but their healing occurrences do not. Any future exact initiative-creation exception requires its own ordering rule.

Next implementation: authentic regular-start receipts and evaluated native opportunities; source-qualified clock descriptors and same-object restoration; conserved missed-output reconciliation; actual parent/concentration and full resource-application transactions. Rapid Coagulation still requires snapshot movement history. The other six major integrations also remain unfinished. Full Time Loop, whole-game closure and GitHub delivery remain pending; no originals were deleted.
'''
    for name in ('README.md','REVIEW_STATUS.md','TEMPORAL_ADAPTER_ENGINEERING_NOTES.md'):
        p=AUDIT/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
    print('Recorded actual22-test bounded closure and two timing clarifications; all seven full integrations remain open.')

if __name__=='__main__':main()
